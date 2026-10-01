import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

export default function ThreeBackground() {
  const mountRef = useRef(null);

  useEffect(() => {
    const currentMount = mountRef.current;
    if (!currentMount) return;

    // Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      60,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    camera.position.z = 80;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: "high-performance" });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    currentMount.appendChild(renderer.domElement);

    // Particles Data
    const particleCount = 120;
    const positions = new Float32Array(particleCount * 3);
    const velocities = [];

    const range = 100;
    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * range;
      positions[i * 3 + 1] = (Math.random() - 0.5) * range;
      positions[i * 3 + 2] = (Math.random() - 0.5) * range * 0.5;

      velocities.push({
        x: (Math.random() - 0.5) * 0.05,
        y: (Math.random() - 0.5) * 0.05,
        z: (Math.random() - 0.5) * 0.03
      });
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    // Particle Texture/Point Material
    const pointMaterial = new THREE.PointsMaterial({
      color: 0x00d2ff,
      size: 1.8,
      transparent: true,
      opacity: 0.85,
      blending: THREE.AdditiveBlending
    });

    const particles = new THREE.Points(geometry, pointMaterial);
    scene.add(particles);

    // Line connections between nearby points
    const maxLines = 150;
    const linePositions = new Float32Array(maxLines * 6);
    const lineColors = new Float32Array(maxLines * 6);
    const lineGeometry = new THREE.BufferGeometry();
    lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3).setUsage(THREE.DynamicDrawUsage));
    lineGeometry.setAttribute('color', new THREE.BufferAttribute(lineColors, 3).setUsage(THREE.DynamicDrawUsage));

    const lineMaterial = new THREE.LineBasicMaterial({
      vertexColors: true,
      transparent: true,
      opacity: 0.4,
      blending: THREE.AdditiveBlending
    });

    const lines = new THREE.LineSegments(lineGeometry, lineMaterial);
    scene.add(lines);

    // Subtle 3D Grid floor (Retro IBM Enterprise mainframe feel)
    const grid = new THREE.GridHelper(200, 30, 0x0f62fe, 0x1e293b);
    grid.position.y = -40;
    grid.material.opacity = 0.2;
    grid.material.transparent = true;
    scene.add(grid);

    // Mouse Interaction
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    const handleMouseMove = (event) => {
      mouseX = (event.clientX / window.innerWidth - 0.5) * 2;
      mouseY = -(event.clientY / window.innerHeight - 0.5) * 2;
    };

    window.addEventListener('mousemove', handleMouseMove, { passive: true });

    // Resize Handler
    const handleResize = () => {
      if (!currentMount) return;
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };

    window.addEventListener('resize', handleResize);

    // Animation Loop
    let animationFrameId;
    const connectionDist = 22;

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      // Smooth camera interpolation
      targetX += (mouseX * 15 - targetX) * 0.05;
      targetY += (mouseY * 10 - targetY) * 0.05;
      camera.position.x = targetX;
      camera.position.y = targetY;
      camera.lookAt(0, 0, 0);

      // Rotate subtle elements
      grid.rotation.y += 0.0006;
      particles.rotation.y += 0.0008;

      const posArray = geometry.attributes.position.array;

      for (let i = 0; i < particleCount; i++) {
        posArray[i * 3] += velocities[i].x;
        posArray[i * 3 + 1] += velocities[i].y;
        posArray[i * 3 + 2] += velocities[i].z;

        // Bounce back inside boundary
        if (Math.abs(posArray[i * 3]) > range / 2) velocities[i].x *= -1;
        if (Math.abs(posArray[i * 3 + 1]) > range / 2) velocities[i].y *= -1;
        if (Math.abs(posArray[i * 3 + 2]) > range / 4) velocities[i].z *= -1;
      }
      geometry.attributes.position.needsUpdate = true;

      // Update dynamic connecting lines
      let lineIndex = 0;
      const lPos = lineGeometry.attributes.position.array;
      const lCol = lineGeometry.attributes.color.array;

      for (let i = 0; i < particleCount && lineIndex < maxLines; i++) {
        const x1 = posArray[i * 3];
        const y1 = posArray[i * 3 + 1];
        const z1 = posArray[i * 3 + 2];

        for (let j = i + 1; j < particleCount && lineIndex < maxLines; j++) {
          const x2 = posArray[j * 3];
          const y2 = posArray[j * 3 + 1];
          const z2 = posArray[j * 3 + 2];

          const dx = x1 - x2;
          const dy = y1 - y2;
          const dz = z1 - z2;
          const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

          if (dist < connectionDist) {
            const alpha = 1.0 - dist / connectionDist;
            
            lPos[lineIndex * 6] = x1;
            lPos[lineIndex * 6 + 1] = y1;
            lPos[lineIndex * 6 + 2] = z1;
            lPos[lineIndex * 6 + 3] = x2;
            lPos[lineIndex * 6 + 4] = y2;
            lPos[lineIndex * 6 + 5] = z2;

            // Gradient cyan to blue line color
            lCol[lineIndex * 6] = 0.0;
            lCol[lineIndex * 6 + 1] = 0.4 * alpha;
            lCol[lineIndex * 6 + 2] = 0.9 * alpha;
            lCol[lineIndex * 6 + 3] = 0.0;
            lCol[lineIndex * 6 + 4] = 0.8 * alpha;
            lCol[lineIndex * 6 + 5] = 1.0 * alpha;

            lineIndex++;
          }
        }
      }

      lineGeometry.setDrawRange(0, lineIndex * 2);
      lineGeometry.attributes.position.needsUpdate = true;
      lineGeometry.attributes.color.needsUpdate = true;

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', handleResize);
      if (currentMount && renderer.domElement) {
        currentMount.removeChild(renderer.domElement);
      }
      geometry.dispose();
      pointMaterial.dispose();
      lineGeometry.dispose();
      lineMaterial.dispose();
      renderer.dispose();
    };
  }, []);

  return (
    <div 
      ref={mountRef} 
      className="fixed inset-0 pointer-events-none z-0 overflow-hidden" 
      aria-hidden="true"
    />
  );
}
