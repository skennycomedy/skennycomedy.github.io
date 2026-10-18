#!/usr/bin/env python3
"""
query_jokes.py

Reads joke search terms and scores line-by-line from clean.txt (or a specified input file),
where each line contains a term and a numeric score separated by a comma (e.g. 'acid,5').
Queries MySQL to find the best match in the jokes table (supporting exact, normalized,
and fuzzy matching). If no match is found, the new/unmatched string is used directly.
Generates SQL INSERT statements:
    insert into jokes (jokeid, score, date, venue) values ('<jokeid>', <score>, '<date>', '<venue>');

The venue and date are supplied via command-line arguments.
The resulting INSERT statements are written to output.sql so they can be piped directly
into MySQL (e.g., `mysql < output.sql`).
"""

import argparse
import difflib
import os
import re
import sys
from datetime import datetime

# Attempt to import pymysql or mysql.connector
try:
    import pymysql
    import pymysql.cursors
    DB_DRIVER = "pymysql"
except ImportError:
    try:
        import mysql.connector
        DB_DRIVER = "mysql.connector"
    except ImportError:
        print("Error: Neither 'pymysql' nor 'mysql.connector' is installed.", file=sys.stderr)
        print("Please install pymysql: pip install pymysql", file=sys.stderr)
        sys.exit(1)


def parse_env_file(filepath=".env.local"):
    """
    Parses a key-value .env file without external dependencies.
    Ignores comments and strips enclosing quotes.
    """
    env_vars = {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip("\"'")
                    env_vars[key] = value
    return env_vars


def get_db_credentials(env_file=".env.local"):
    """Returns database configuration dict from env file and environment variables."""
    env = parse_env_file(env_file)
    user = env.get("USER") or os.environ.get("USER")
    password = env.get("PASS") or env.get("PASSWORD") or os.environ.get("PASS") or os.environ.get("PASSWORD")
    db_name = env.get("DB") or env.get("DATABASE") or os.environ.get("DB") or os.environ.get("DATABASE")
    host = env.get("HOST", "127.0.0.1")
    port = int(env.get("PORT", 3306))
    return {
        "user": user,
        "password": password,
        "database": db_name,
        "host": host,
        "port": port,
    }


def get_db_connection(creds):
    """Establishes and returns a connection based on credentials dict."""
    user = creds.get("user")
    db_name = creds.get("database")
    if not user or not db_name:
        print("Error: Database user or database name missing in configuration.", file=sys.stderr)
        sys.exit(1)

    if DB_DRIVER == "pymysql":
        return pymysql.connect(
            host=creds.get("host", "127.0.0.1"),
            port=creds.get("port", 3306),
            user=user,
            password=creds.get("password"),
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor,
            charset="utf8mb4",
        )
    else:
        return mysql.connector.connect(
            host=creds.get("host", "127.0.0.1"),
            port=creds.get("port", 3306),
            user=user,
            password=creds.get("password"),
            database=db_name,
            dictionary=True,
        )


def clean_term(s):
    """Strips parenthetical notes such as '(long pause on exist)' or '(+ new sarah?)'."""
    s = re.sub(r"\(.*?\)", "", s)
    return s.strip()


def normalize(s):
    """
    Normalizes a string by removing punctuation and converting
    whitespace/symbols into single underscores, lowercased.
    E.g. 'ai poetry' -> 'ai_poetry', 'counseling + folta' -> 'counseling_folta'
    """
    cleaned = clean_term(s)
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", cleaned)
    return slug.strip("_").lower()


def get_tokens(s):
    """Returns a list of lowercase alphanumeric word tokens."""
    cleaned = clean_term(s)
    tokens = re.findall(r"[a-zA-Z0-9]+", cleaned.lower())
    return [t for t in tokens if t]


def find_best_jokeid(term, all_jokeids, threshold=0.70):
    """
    Finds the single best matching jokeid from the database for a search term.
    Tiers:
    1. Exact match (case-insensitive)
    2. Normalized match (spaces/symbols <-> underscores)
    3. Token containment (all search words present in candidate jokeid)
    4. Fuzzy similarity (edit distance / ratio)
    """
    cleaned = clean_term(term)
    norm_term = normalize(term)
    tokens = get_tokens(term)

    # 1. Exact match (case-insensitive)
    for j in all_jokeids:
        if j.lower() == term.lower() or j.lower() == cleaned.lower():
            return "exact", j

    # 2. Normalized match (spaces/punctuation <-> underscores)
    for j in all_jokeids:
        if normalize(j) == norm_term:
            return "normalized", j

    # 3. Token containment (all search words present in candidate)
    if len(tokens) > 1:
        token_matches = [j for j in all_jokeids if all(t in get_tokens(j) for t in tokens)]
        if token_matches:
            token_matches.sort(key=lambda x: (len(x), x))
            return "token", token_matches[0]

    # 4. Fuzzy similarity (edit distance / ratio)
    scores = []
    for j in all_jokeids:
        score = difflib.SequenceMatcher(None, norm_term, normalize(j)).ratio()
        if score >= threshold:
            scores.append((score, j))

    if scores:
        scores.sort(key=lambda x: x[0], reverse=True)
        return "fuzzy", scores[0][1]

    return "none", None


def escape_sql(value):
    """Escapes single quotes for standard SQL literals."""
    return str(value).replace("'", "''")


def parse_date(date_str):
    """
    Parses a user-supplied date string into MySQL YYYY-MM-DD format.
    Defaults to current date if omitted or invalid.
    """
    if not date_str:
        return datetime.now().strftime("%Y-%m-%d")
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y", "%Y/%m/%d", "%b %d %Y", "%B %d %Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return date_str.strip()


def parse_line(line):
    """
    Parses a line from clean.txt into (term, score_str).
    Expects comma-separated format: 'term,score'.
    If no comma is present, returns (term, None).
    """
    line = line.strip()
    if not line:
        return None, None
    if "," in line:
        term, score_str = line.rsplit(",", 1)
        term = term.strip()
        score_str = score_str.strip()
    else:
        term = line
        score_str = None
    return term, score_str


def format_score_literal(score_str):
    """Formats score value for SQL insert: numeric literal or NULL."""
    if score_str is None or score_str == "":
        return "NULL"
    if score_str.isdigit():
        return score_str
    try:
        float(score_str)
        return score_str
    except ValueError:
        return f"'{escape_sql(score_str)}'"


def format_insert_sql(jokeid, score_str, date_str, venue, table="jokes"):
    """
    Formats the SQL INSERT statement.
    Default table is 'jokes', producing:
    insert into jokes (jokeid, score, date, venue) values ('<jokeid>', <score>, '<date>', '<venue>');
    """
    table_part = f"{table} " if table else ""
    score_literal = format_score_literal(score_str)
    return (
        f"insert into {table_part}(jokeid, score, date, venue) "
        f"values ('{escape_sql(jokeid)}', {score_literal}, '{escape_sql(date_str)}', '{escape_sql(venue)}');"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Query jokes in MySQL and generate executable SQL INSERT statements for output.sql."
    )
    parser.add_argument(
        "venue_pos",
        nargs="?",
        default=None,
        metavar="VENUE",
        help="Venue name (positional argument)"
    )
    parser.add_argument(
        "-v", "--venue",
        default=None,
        help="Venue name for generated insert statements (e.g. -v 'westside')"
    )
    parser.add_argument(
        "-d", "--date",
        default=None,
        help="Date for insert statements in YYYY-MM-DD format (defaults to today's date if omitted)"
    )
    parser.add_argument(
        "-i", "--input",
        default="clean.txt",
        help="Path to input text file (default: clean.txt)"
    )
    parser.add_argument(
        "-o", "--output",
        default="output.sql",
        help="Path to output SQL file (default: output.sql)"
    )
    parser.add_argument(
        "--table",
        default="jokes",
        help="Table name to include in 'insert into <table>' (default: 'jokes')"
    )
    parser.add_argument(
        "--use-db",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include 'USE <dbname>;' at the top of the SQL file (default: True, use --no-use-db to omit)"
    )
    parser.add_argument(
        "--env",
        default=".env.local",
        help="Path to environment file (default: .env.local)"
    )
    parser.add_argument(
        "--no-fuzzy",
        action="store_true",
        help="Disable fuzzy/normalized matching and require exact matches."
    )
    parser.add_argument(
        "-t", "--threshold",
        type=float,
        default=0.70,
        help="Fuzzy similarity threshold (0.0 to 1.0, default: 0.70)"
    )
    args = parser.parse_args()

    venue = args.venue or args.venue_pos
    if not venue:
        print("Error: Venue must be provided on the command line.", file=sys.stderr)
        print("Example: python3 query_jokes.py -v 'westside' -d '2026-10-17'", file=sys.stderr)
        print("         python3 query_jokes.py 'westside'", file=sys.stderr)
        sys.exit(1)

    target_date = parse_date(args.date)

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    # Read entries from input file
    entries = []
    with open(args.input, "r", encoding="utf-8") as f:
        for line in f:
            term, score = parse_line(line)
            if term:
                entries.append((term, score))

    print(f"Connecting to database using settings from '{args.env}'...")
    try:
        creds = get_db_credentials(args.env)
        conn = get_db_connection(creds)
    except Exception as e:
        print(f"Connection failed: {e}", file=sys.stderr)
        sys.exit(1)

    db_name = creds.get("database")

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT jokeid FROM jokes WHERE jokeid IS NOT NULL")
            all_jokeids = [r["jokeid"] for r in cursor.fetchall()]
    finally:
        conn.close()

    print(f"Loaded {len(entries)} items from '{args.input}'.")
    print(f"Venue: '{venue}' | Date: '{target_date}' | Target Table: '{args.table}'")
    print(f"Indexed {len(all_jokeids)} distinct jokeids in database.")
    print(f"Processing and generating INSERT statements...\n" + "=" * 80)

    generated_statements = []
    matched_count = 0
    new_unmatched_count = 0

    for term, score in entries:
        # Check exact or fuzzy match in database
        if args.no_fuzzy:
            cleaned = clean_term(term)
            matched_jid = next((j for j in all_jokeids if j.lower() == term.lower() or j.lower() == cleaned.lower()), None)
            match_type = "exact" if matched_jid else "none"
        else:
            match_type, matched_jid = find_best_jokeid(term, all_jokeids, threshold=args.threshold)

        if matched_jid:
            jokeid_to_use = matched_jid
            matched_count += 1
            status_tag = f"MATCH - {match_type.capitalize()}"
        else:
            # Fall back to new, unmatched string
            jokeid_to_use = term
            new_unmatched_count += 1
            status_tag = "NEW - No Match"

        sql = format_insert_sql(jokeid_to_use, score, target_date, venue, table=args.table)
        generated_statements.append(sql)

        score_display = score if score is not None else "N/A"
        print(f"[{status_tag:<18}] '{term}' -> '{jokeid_to_use}' (score: {score_display})")
        print(f"  SQL: {sql}")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total lines processed:     {len(entries)}")
    print(f"Matched in database:       {matched_count}")
    print(f"New / unmatched strings:   {new_unmatched_count}")
    print(f"Total statements generated:{len(generated_statements)}")

    # Write SQL statements to output file
    with open(args.output, "w", encoding="utf-8") as out:
        if args.use_db and db_name:
            out.write(f"USE `{escape_sql(db_name)}`;\n\n")
        for stmt in generated_statements:
            out.write(stmt + "\n")

    print(f"Wrote {len(generated_statements)} INSERT statements to '{args.output}'.")


if __name__ == "__main__":
    main()
