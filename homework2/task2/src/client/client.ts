import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { ModelVisualization } from "./vis";
import Model from "./model";

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
const axesHelper = new THREE.AxesHelper(3);
scene.add(axesHelper);

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

  // if (curTime != undefined) {
  //   render();
  //   return;
  // }
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

  render();
}

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function render() {
  renderer.render(scene, camera);
}

animate();
