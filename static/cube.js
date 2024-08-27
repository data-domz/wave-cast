document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('cube-container');
    const width = container.clientWidth;
    const height = container.clientHeight || 600; // Increased default height

    // Create a scene
    const scene = new THREE.Scene();

    // Create a camera
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.z = 15; // Move the camera further back to make the objects appear larger

    // Create a renderer with alpha enabled for transparency
    const renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setClearColor(0x000000, 0); // Set clear color to transparent
    renderer.setSize(width, height);
    container.appendChild(renderer.domElement);

    // Create a standard cube geometry and a wireframe material
    const cubeGeometry = new THREE.BoxGeometry(6, 6, 6);
    const cubeEdges = new THREE.EdgesGeometry(cubeGeometry);
    const cubeMaterial = new THREE.LineBasicMaterial({ color: 0x00ff00 });
    const cubeWireframe = new THREE.LineSegments(cubeEdges, cubeMaterial);

    // Create a cube mesh
    scene.add(cubeWireframe);

    // Create a larger surfboard shape
    const surfboardShape = new THREE.Shape();
    surfboardShape.moveTo(0, 4); // Increased size
    surfboardShape.quadraticCurveTo(2, 4, 2, 2);
    surfboardShape.quadraticCurveTo(2, -2, 0, -4);
    surfboardShape.quadraticCurveTo(-2, -2, -2, 2);
    surfboardShape.quadraticCurveTo(-2, 4, 0, 4);

    const extrudeSettings = {
        steps: 2,
        depth: 0.4, // Increased depth
        bevelEnabled: true,
        bevelThickness: 0.2,
        bevelSize: 0.2,
        bevelSegments: 1
    };

    // Create the red surfboard mesh
    const surfboardGeometry = new THREE.ExtrudeGeometry(surfboardShape, extrudeSettings);
    const surfboardMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
    const surfboard = new THREE.Mesh(surfboardGeometry, surfboardMaterial);
    surfboard.rotation.x = Math.PI / 2;
    surfboard.position.z = 1;
    scene.add(surfboard);

    // Create the white outline
    const outlineMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.BackSide });
    const outlineMesh = new THREE.Mesh(surfboardGeometry, outlineMaterial);
    outlineMesh.scale.set(1.05, 1.05, 1.05); // Slightly larger to appear as an outline
    surfboard.add(outlineMesh);

    // Create the stringer
    const stringerShape = new THREE.Shape();
    stringerShape.moveTo(0, 4);
    stringerShape.lineTo(0, -4);

    const stringerPoints = stringerShape.getPoints(2);
    const stringerGeometry = new THREE.BufferGeometry().setFromPoints(stringerPoints);
    const stringerMaterial = new THREE.LineBasicMaterial({ color: 0xffffff });
    const stringer = new THREE.Line(stringerGeometry, stringerMaterial);
    stringer.position.z = 0.2; // Adjust the position to ensure it aligns correctly
    surfboard.add(stringer); // Add the stringer as a child of the surfboard

    // Create an animation loop
    function animate() {
        requestAnimationFrame(animate);

        // Rotate the cube
        cubeWireframe.rotation.x += 0.01;
        cubeWireframe.rotation.y += 0.01;

        // Rotate the surfboard
        surfboard.rotation.x += 0.01;
        surfboard.rotation.y += 0.01;

        // Render the scene
        renderer.render(scene, camera);
    }

    animate();
});
