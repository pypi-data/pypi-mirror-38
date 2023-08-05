var canvas = document.getElementById("renderCanvas");
var engine = new BABYLON.Engine(canvas);
var scene = new BABYLON.Scene(engine);

scene.createDefaultCamera(true, true, true);
scene.createDefaultLight(true);
scene.createDefaultEnvironment({
  skyboxSize: 50,
  enableGroundShadow: false
});

var lightDir = new BABYLON.Vector3(-0.5, -1, 0.1);
var light = new BABYLON.DirectionalLight("DirectionalLight", lightDir, scene);
light.position = new BABYLON.Vector3(5, 40, 0);
var shadowGenerator = new BABYLON.ShadowGenerator(1024, light);
shadowGenerator.useExponentialShadowMap = true;

scene.activeCamera.setTarget(new BABYLON.Vector3(0, 7, 0));
scene.activeCamera.setPosition(new BABYLON.Vector3(0, 11.5, -15));
scene.activeCamera.fov = 0.5;
scene.activeCamera.useAutoRotationBehavior = true;
scene.activeCamera.autoRotationBehavior.idleRotationSpeed = Math.PI / 4;

BABYLON.SceneLoader.Append("", "drum3.glb", scene, function(scene) {
  var table = scene.rootNodes[4].getChildren()[0];
  var pedestal = table.getChildren()[0];
  var hat = pedestal.getChildren()[0];

  shadowGenerator.addShadowCaster(pedestal);
  shadowGenerator.addShadowCaster(hat);
  table.receiveShadows = true;
  pedestal.receiveShadows = true;

  engine.runRenderLoop(function() {
    scene.render();
  });
});

// setup onclick
document.onclick = () => {
  document.getElementById("leftCurtain").classList.add("curtains-open-left");
  document.getElementById("rightCurtain").classList.add("curtains-open-right");

  var floatingText = document.getElementById("floatingText");
  floatingText.parentNode.removeChild(floatingText);

  var audio = new Audio("applause4.wav");
  audio.play();
  document.onclick = null;
}

//confetti
function animate() {
  requestAnimationFrame(animate);

  confetti({
    particleCount: 5,
    angle: 60,
    spread: 55,
    origin: {
      x: 0
    }
  });
  confetti({
    particleCount: 5,
    angle: 120,
    spread: 55,
    origin: {
      x: 1
    }
  });
}

animate();
