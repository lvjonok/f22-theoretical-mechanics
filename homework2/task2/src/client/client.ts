import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { ModelVisualization, updateLabel } from "./vis";
import Model from "./model";
import { Vector } from "./vector";

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
camera.position.z = 20;
camera.up = new THREE.Vector3(0, 0, 1);

const canvas = document.querySelector("#c") as HTMLCanvasElement;
const renderer = new THREE.WebGLRenderer({ canvas });
renderer.setSize(window.innerWidth, window.innerHeight);

// document.body.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);

const initModel = new Model(0);

// add axes

const Xhelper = new Vector(
  new THREE.Vector3(0, 0, 0),
  new THREE.Vector3(3, 0, 0),
  0xff0000
);
scene.add(Xhelper);

const Yhelper = new Vector(
  new THREE.Vector3(0, 0, 0),
  new THREE.Vector3(0, 3, 0),
  0x00ff00
);
scene.add(Yhelper);

const Zhelper = new Vector(
  new THREE.Vector3(0, 0, 0),
  new THREE.Vector3(0, 0, 3),
  0x0000ff
);
scene.add(Zhelper);

// add labels to axesHelper
const labels = document.querySelector("#static-labels") as HTMLDivElement;
const divX = document.createElement("div");
divX.textContent = "X";
labels.appendChild(divX);
const divY = document.createElement("div");
divY.textContent = "Y";
labels.appendChild(divY);
const divZ = document.createElement("div");
divZ.textContent = "Z";
labels.appendChild(divZ);

window.addEventListener("resize", onWindowResize, false);
function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  render();
}

let startTime = Date.now();
let curTime: number;

let prevModel: Model | undefined = undefined;

var visualModel: ModelVisualization;

function animate() {
  if (!prevModel) {
    visualModel ? visualModel.remove(scene) : null;
    visualModel = new ModelVisualization(initModel, scene);
  }
  requestAnimationFrame(animate);

  curTime = Date.now();
  const timeDelta = (curTime - startTime) / 10000.0; // in seconds

  console.log(timeDelta);
  if (timeDelta > 2.0) {
    startTime = Date.now();
    prevModel = undefined;
    return;
  }

  const model = new Model(timeDelta, prevModel);
  prevModel = model;

  visualModel.update(model, camera);

  // // rotate cone around its axis
  // visualModel.coneA.rotateOnWorldAxis(
  //   new THREE.Vector3(0, -Math.cos(Math.PI / 4), -Math.sin(Math.PI / 4)),
  //   0.01
  // );

  updateLabel(Xhelper, divX, camera, canvas);
  updateLabel(Yhelper, divY, camera, canvas);
  updateLabel(Zhelper, divZ, camera, canvas);

  render();
}

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function render() {
  renderer.render(scene, camera);
}

animate();
