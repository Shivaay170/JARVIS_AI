import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# System states
latest_scan = {
    "object_name": "Awaiting System Scan...",
    "object_type": "None",
    "confidence_score": 0.0,
    "primary_materials": []
}

# 0.0 = Assembled, 1.0 = Fully Exploded into layers
system_control = {
    "explosion_factor": 0.0
}

class ControlSchema(BaseModel):
    explosion_factor: float

@app.post("/api/scan")
async def receive_scan(data: dict):
    global latest_scan
    latest_scan = data
    print(f"[JARVIS SERVER] Target matrix updated -> {data['object_name']}")
    return {"status": "success"}

@app.get("/api/scan")
async def get_latest_scan():
    return latest_scan

@app.post("/api/control")
async def update_control(control: ControlSchema):
    global system_control
    system_control["explosion_factor"] = control.explosion_factor
    return {"status": "control_updated"}

@app.get("/api/control")
async def get_control():
    return system_control

@app.get("/", response_class=HTMLResponse)
async def live_hud_interface():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>JARVIS - Holographic Interface Matrix</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <style>
            body {
                margin: 0;
                background-color: #02070f;
                color: #00ffcc;
                font-family: 'Courier New', Courier, monospace;
                overflow: hidden;
            }
            #hud-overlay {
                position: absolute;
                top: 20px;
                left: 20px;
                background: rgba(4, 18, 36, 0.85);
                padding: 20px;
                border: 1px solid #00ffcc;
                border-radius: 6px;
                box-shadow: 0 0 20px rgba(0, 255, 204, 0.25);
                pointer-events: none;
                width: 320px;
                z-index: 10;
            }
            #manual-deck {
                position: absolute;
                bottom: 20px;
                left: 20px;
                background: rgba(4, 18, 36, 0.85);
                padding: 15px;
                border: 1px solid #ffaa00;
                border-radius: 6px;
                width: 320px;
                z-index: 10;
            }
            h2 { margin-top: 0; color: #ffffff; font-size: 1.1rem; border-bottom: 1px solid #00ffcc; padding-bottom: 5px; }
            .metric { margin: 8px 0; font-size: 0.9rem; }
            .val { color: #ffffff; font-weight: bold; }
            input[type=range] { width: 100%; accent-color: #ffaa00; }
            label { font-size: 0.8rem; color: #ffaa00; }
        </style>
    </head>
    <body>

        <div id="hud-overlay">
            <h2>HOLOGRAPHIC RECONSTRUCTION</h2>
            <div class="metric">TARGET: <span id="target-name" class="val">Loading...</span></div>
            <div class="metric">CLASS: <span id="target-type" class="val">-</span></div>
            <div class="metric">MATRIX CONFIDENCE: <span id="target-conf" class="val">-</span></div>
            <div class="metric">SURFACE MATERIAL: <span id="target-mat" class="val">-</span></div>
        </div>

        <div id="manual-deck">
            <label>TEARDOWN INTERFACE MATRIX DEBUGGER</label>
            <input type="range" id="explosion-slider" min="0" max="100" value="0">
        </div>

        <script>
            // ── THREE.JS SCENE CONFIGURATION ─────────────────────────────────
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // Add subtle diagnostic lighting layers
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
            scene.add(ambientLight);
            const directionalLight = new THREE.DirectionalLight(0x00ffcc, 0.8);
            directionalLight.position.set(5, 5, 5);
            scene.add(directionalLight);

            // Master structural assembly container
            const assemblyGroup = new THREE.Group();
            scene.add(assemblyGroup);

            // ── GENERATE LAYER DATA (CINEMATIC DIGITAL TWIN) ─────────────────
            function createLayer(w, h, d, color, wireColor, opacity) {
                const geo = new THREE.BoxGeometry(w, h, d);
                const mat = new THREE.MeshPhongMaterial({
                    color: color,
                    transparent: true,
                    opacity: opacity,
                    side: THREE.DoubleSide
                });
                const mesh = new THREE.Mesh(geo, mat);

                const wireGeo = new THREE.WireframeGeometry(geo);
                const wireMat = new THREE.LineBasicMaterial({ color: wireColor, linewidth: 1.5 });
                const wireframe = new THREE.LineSegments(wireGeo, wireMat);
                
                mesh.add(wireframe);
                return mesh;
            }

            // Instantiate components sequentially along the structural layout core
            const layer1_Screen  = createLayer(2.0, 3.8, 0.04, 0x00aaff, 0x00ffff, 0.25);
            const layer2_Circuit = createLayer(1.8, 3.5, 0.05, 0x00ffaa, 0x00ff88, 0.60);
            const layer3_Battery = createLayer(1.4, 2.2, 0.12, 0xffaa00, 0xff5500, 0.50);
            const layer4_Chassis = createLayer(2.02, 3.82, 0.08, 0x004488, 0x0066cc, 0.30);

            // Attach internal circuit details onto the logic board layer
            const chipGeo = new THREE.BoxGeometry(0.4, 0.4, 0.1);
            const chipMat = new THREE.MeshPhongMaterial({ color: 0xff0055 });
            const chip = new THREE.Mesh(chipGeo, chipMat);
            chip.position.set(0.2, 0.8, 0.05);
            layer2_Circuit.add(chip);

            assemblyGroup.add(layer1_Screen);
            assemblyGroup.add(layer2_Circuit);
            assemblyGroup.add(layer3_Battery);
            assemblyGroup.add(layer4_Chassis);

            camera.position.set(2.5, 2, 4.5);
            camera.lookAt(0, 0, 0);

            // Global runtime pointer state variable
            let targetExplosionFactor = 0.0;
            let currentExplosionFactor = 0.0;

            // ── RENDERING & KINETIC EXPLOSION MECHANICS ──────────────────────
            function animate() {
                requestAnimationFrame(animate);

                // Smoothly ease matching transition steps
                currentExplosionFactor += (targetExplosionFactor - currentExplosionFactor) * 0.1;

                // Separate layers along the depth axis (Z-Axis) matching engineering schemas
                layer1_Screen.position.z  = currentExplosionFactor * 1.5;
                layer2_Circuit.position.z = currentExplosionFactor * 0.4;
                layer3_Battery.position.z = currentExplosionFactor * -0.4;
                layer4_Chassis.position.z = currentExplosionFactor * -1.5;

                // Slow rotation loop to appreciate the depth dimensions
                assemblyGroup.rotation.y += 0.006;
                
                renderer.render(scene, camera);
            }
            animate();

            // ── DATA INTERCEPT & INTERACTION MANAGEMENT ──────────────────────
            const slider = document.getElementById('explosion-slider');
            let sliderControlled = false;

            slider.addEventListener('input', (e) => {
                sliderControlled = true;
                targetExplosionFactor = e.target.value / 100;
            });

            async function pollTelemetry() {
                try {
                    // Pull object metrics
                    const scanResponse = await fetch('/api/scan');
                    const scanData = await scanResponse.json();
                    document.getElementById('target-name').innerText = scanData.object_name;
                    document.getElementById('target-type').innerText = scanData.object_type;
                    document.getElementById('target-conf').innerText = (scanData.confidence_score * 100).toFixed(0) + '%';
                    document.getElementById('target-mat').innerText = scanData.primary_materials.join(', ');

                    // Pull external server control states (if updated via API)
                    if (!sliderControlled) {
                        const ctrlResponse = await fetch('/api/control');
                        const ctrlData = await ctrlResponse.json();
                        targetExplosionFactor = ctrlData.explosion_factor;
                        slider.value = ctrlData.explosion_factor * 100;
                    }
                } catch (err) {
                    console.error("Telemetry link tracking offline:", err);
                }
            }
            setInterval(pollTelemetry, 400);

            window.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)