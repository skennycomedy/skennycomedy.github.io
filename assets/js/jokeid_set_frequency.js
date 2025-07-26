<div id="threejs-container" style="width: 100%; height: 500px;"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/FontLoader.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/fonts/helvetiker_regular.typeface.json"></script>
<script>
    // Function to read and parse the CSV file
    function loadCSV(url) {
        return fetch(url)
            .then(response => response.text())
            .then(csvText => {
                const rows = csvText.split('\n').slice(1);
                const data = rows.map(row => {
                    const [name, freq] = row.split(',');
                    if (name && freq) {
                        return { name: name.trim(), freq: parseInt(freq.trim()) };
                    }
                }).filter(item => item && !isNaN(item.freq));
                return data;
            });
    }

    // Main function to set up the Three.js scene
    function createScene(data) {
        const container = document.getElementById('threejs-container');
        
        // Create scene, camera, and renderer
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x4B5320);

        const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(0, 20, 30);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.shadowMap.enabled = true;

        // Append the renderer to the div container
        container.appendChild(renderer.domElement);

        // OrbitControls setup
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.screenSpacePanning = false;
        controls.maxPolarAngle = Math.PI / 2;
        controls.update();

        // Lighting setup
        const ambientLight = new THREE.AmbientLight(0x404040, 2);
        scene.add(ambientLight);

        const pointLight = new THREE.PointLight(0xffffff, 1);
        pointLight.position.set(10, 10, 40);
        pointLight.castShadow = true;
        scene.add(pointLight);

        // Plane setup with pink floor and canvas texture
        const canvas = document.createElement('canvas');
        const canvasWidth = 2048;
        const canvasHeight = 1024;
        canvas.width = canvasWidth;
        canvas.height = canvasHeight;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#FF69B4';
        ctx.fillRect(0, 0, canvasWidth, canvasHeight);

        const texture = new THREE.CanvasTexture(canvas);
        const planeGeometry = new THREE.PlaneGeometry(60, 30);
        const planeMaterial = new THREE.MeshPhongMaterial({ map: texture, side: THREE.DoubleSide });
        const plane = new THREE.Mesh(planeGeometry, planeMaterial);
        plane.rotation.x = -Math.PI / 2;
        plane.position.y = 0;
        plane.receiveShadow = true;
        scene.add(plane);

        // Load the font for 3D text
        const fontLoader = new THREE.FontLoader();
        fontLoader.load('https://cdn.jsdelivr.net/npm/three@0.128.0/examples/fonts/helvetiker_regular.typeface.json', (font) => {
            const textGeometry = new THREE.TextGeometry('JokeID Group Frequency', {
                font: font,
                size: 2,
                height: 1.5,
                curveSegments: 12,
                bevelEnabled: false
            });

            const textMaterial = new THREE.MeshPhongMaterial({ color: 0xFFFF00 });
            const textMesh = new THREE.Mesh(textGeometry, textMaterial);

            textMesh.rotation.x = 0;
            textMesh.position.set(0, 5, -15);
            textMesh.castShadow = true;

            scene.add(textMesh);
        });

        // Bars creation and labels
        const bars = [];
        const maxBarHeight = Math.max(...data.map(item => item.freq));
        const fontLoader2 = new THREE.FontLoader();
        fontLoader2.load('https://cdn.jsdelivr.net/npm/three@0.128.0/examples/fonts/helvetiker_regular.typeface.json', (font) => {
            data.forEach((item, index) => {
                const finalBarHeight = item.freq / maxBarHeight * 15;
                const geometry = new THREE.BoxGeometry(1.5, 1, 1.5);
                const material = new THREE.MeshPhongMaterial({ color: 0x0077ff, shininess: 100, specular: 0x333333 });
                const bar = new THREE.Mesh(geometry, material);
                bar.castShadow = true;

                bar.position.x = index * 3 - (data.length * 3) / 2 + 1.5;
                bar.position.y = 0.5;
                bar.position.z = 0;
                scene.add(bar);

                bars.push({
                    mesh: bar,
                    targetHeight: finalBarHeight,
                    currentScale: 1,
                });

                // Create 3D text labels for each bar using the loaded font
                const textGeometry = new THREE.TextGeometry(item.name, {
                    font: font,
                    size: 0.7,
                    height: 0.1,
                    curveSegments: 12,
                    bevelEnabled: false
                });

                const textMaterial = new THREE.MeshPhongMaterial({ color: 0xFFFF00 });
                const textMesh = new THREE.Mesh(textGeometry, textMaterial);

                textMesh.rotation.x = -Math.PI / 2;
                textMesh.rotation.y = Math.PI / 2;
                textMesh.rotation.z = Math.PI / 2;
                textMesh.position.set(bar.position.x + .8, 0.95, bar.position.z + 14.5);
                textMesh.castShadow = true;

                scene.add(textMesh);
            });
        });

        // Animation loop
        function animate() {
            requestAnimationFrame(animate);
            bars.forEach(barData => {
                if (barData.currentScale < barData.targetHeight) {
                    barData.currentScale += 0.1;
                    barData.mesh.scale.y = barData.currentScale / barData.mesh.geometry.parameters.height;
                    barData.mesh.position.y = barData.currentScale / 2;
                }
            });
            controls.update();
            renderer.render(scene, camera);
        }
        animate();

        // Handle window resizing
        window.addEventListener('resize', () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });
    }

    // Load data and initialize the scene
    loadCSV('/wp-content/uploads/2024/02/joke_data.csv').then(data => {
        createScene(data);
    });
</script>
