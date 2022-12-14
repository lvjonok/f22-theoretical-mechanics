import * as THREE from "three";
import Model, { alphaA, OM0 } from "./model";
import { Vector } from "./vector";
import { coneAstartAxis, alphaB } from "./model";
import { MathUtils, Scene } from "three";

const tempV = new THREE.Vector3();

export class ModelVisualization {
  private model: Model;

  coneA: THREE.Mesh;
  coneB: THREE.Mesh;

  posM: THREE.Mesh;
  posMlabel: HTMLDivElement;
  velM: Vector;
  velMlabel: HTMLDivElement;
  accM: Vector;
  accMlabel: HTMLDivElement;
  accMt: Vector;
  accMtlabel: HTMLDivElement;
  accMn: Vector;
  accMnlabel: HTMLDivElement;

  angVelA: Vector;
  angVelAlabel: HTMLDivElement;
  angAccA: Vector;
  angAccAlabel: HTMLDivElement;

  labels: HTMLDivElement;
  objLabels: { [idx: number]: { html: HTMLDivElement; obj: THREE.Object3D } } =
    {};
  // wA: Vector;

  constructor(private init: Model, scene: THREE.Scene) {
    this.labels = document.querySelector("#labels") as HTMLDivElement;
    this.labels.innerHTML = "";

    this.model = init;

    this.coneB = CreateCone(
      new THREE.Vector3(0, 0, 0),
      new THREE.Vector3(0, 0, -1),
      OM0 * Math.sin(MathUtils.degToRad(alphaB / 2)),
      OM0 * Math.cos(MathUtils.degToRad(alphaB / 2))
    );
    this.coneB.name = "coneB";
    scene.add(this.coneB);

    this.coneA = CreateCone(
      new THREE.Vector3(0, 0, 0),
      coneAstartAxis,
      OM0 * Math.sin(MathUtils.degToRad(alphaA / 2)),
      OM0 * Math.cos(MathUtils.degToRad(alphaA / 2)),
      0xff0000
    );
    this.coneA.name = "coneA";
    scene.add(this.coneA);

    this.posM = CreatePoint(new THREE.Vector3(0, 0, 0));
    scene.add(this.posM);
    const div = document.createElement("div");
    div.textContent = "posM";
    this.labels.appendChild(div);
    this.posMlabel = div;

    this.velM = new Vector(new THREE.Vector3(), new THREE.Vector3(), 0xfffff00);
    scene.add(this.velM);
    const div2 = document.createElement("div");
    div2.textContent = "velM";
    this.labels.appendChild(div2);
    this.velMlabel = div2;

    this.accM = new Vector(new THREE.Vector3(), new THREE.Vector3(), 0x00ffff);
    scene.add(this.accM);
    const div3 = document.createElement("div");
    div3.textContent = "accM";
    this.labels.appendChild(div3);
    this.accMlabel = div3;

    this.angVelA = new Vector(
      new THREE.Vector3(),
      new THREE.Vector3(),
      0xff00ff
    );
    scene.add(this.angVelA);
    const div4 = document.createElement("div");
    div4.textContent = "angVelA";
    this.labels.appendChild(div4);
    this.angVelAlabel = div4;

    this.angAccA = new Vector(
      new THREE.Vector3(),
      new THREE.Vector3(),
      0xffffff
    );
    scene.add(this.angAccA);
    const div5 = document.createElement("div");
    div5.textContent = "angAccA";
    this.labels.appendChild(div5);
    this.angAccAlabel = div5;

    this.accMt = new Vector(new THREE.Vector3(), new THREE.Vector3(), 0x00ff00);
    scene.add(this.accMt);
    const div6 = document.createElement("div");
    div6.textContent = "accMt";
    this.labels.appendChild(div6);
    this.accMtlabel = div6;

    this.accMn = new Vector(new THREE.Vector3(), new THREE.Vector3(), 0xff0000);
    scene.add(this.accMn);
    const div7 = document.createElement("div");
    div7.textContent = "accMn";
    this.labels.appendChild(div7);
    this.accMnlabel = div7;

    this.updVis();
  }

  update(model: Model, camera?: THREE.Camera) {
    this.model = model;
    this.updVis(camera);
  }

  remove(scene: THREE.Scene) {
    scene.remove(this.coneA);
    scene.remove(this.coneB);
    scene.remove(this.posM);
    scene.remove(this.velM);
    scene.remove(this.accM);
    scene.remove(this.angVelA);
    scene.remove(this.angAccA);
    scene.remove(this.accMt);
    scene.remove(this.accMn);
  }

  // method updates positions of all objects on current model
  private updVis(camera?: THREE.Camera) {
    const canvas = document.querySelector("#c") as HTMLCanvasElement;

    this.coneA.applyMatrix4(
      RotationFromTo(
        this.model.prev ? this.model.prev.axisA : coneAstartAxis,
        this.model.axisA
      )
    );

    const tempV = new THREE.Vector3();

    this.posM.position.set(
      this.model.posM.x,
      this.model.posM.y,
      this.model.posM.z
    );

    this.velM?.setOrigin(this.model.posM);
    this.velM?.setEnd(this.model.posM.clone().add(this.model.velM));

    this.accM?.setOrigin(this.model.posM);
    this.accM?.setEnd(this.model.posM.clone().add(this.model.accM));

    this.angVelA.setEnd(this.model.angVelA);
    this.angAccA.setEnd(this.model.angAccA);

    this.accMt?.setOrigin(this.model.posM);
    this.accMt?.setEnd(this.model.posM.clone().add(this.model.accMt));

    this.accMn?.setOrigin(this.model.posM);
    this.accMn?.setEnd(this.model.posM.clone().add(this.model.accMn));

    if (camera) {
      updateLabel(this.posM, this.posMlabel, camera, canvas);
      updateLabel(this.velM, this.velMlabel, camera, canvas);
      updateLabel(this.accM, this.accMlabel, camera, canvas);
      updateLabel(this.accMt, this.accMtlabel, camera, canvas);
      updateLabel(this.accMn, this.accMnlabel, camera, canvas);
      updateLabel(this.angVelA, this.angVelAlabel, camera, canvas);
      updateLabel(this.angAccA, this.angAccAlabel, camera, canvas);
    }
  }
}

function RotationFromTo(from: THREE.Vector3, to: THREE.Vector3) {
  const axis = new THREE.Vector3();
  axis.crossVectors(from, to);
  axis.normalize();
  const angle = Math.acos(from.dot(to) / (from.length() * to.length()));
  return new THREE.Matrix4().makeRotationAxis(axis, angle);
}

// create cone object
function CreateCone(
  vertex: THREE.Vector3,
  direction: THREE.Vector3,
  radius: number,
  height: number,
  color?: THREE.ColorRepresentation
) {
  const geometry = new THREE.ConeGeometry(radius, height, 32, 32, true);
  const material = new THREE.MeshBasicMaterial({
    color: color ? color : 0xffff00,
    wireframe: true,
  });
  const cone = new THREE.Mesh(geometry, material);
  cone.translateY(-height / 2);
  cone.applyMatrix4(
    new THREE.Matrix4().makeBasis(
      new THREE.Vector3(0, 1, 0),
      new THREE.Vector3(0, 0, 1),
      new THREE.Vector3(1, 0, 0)
    )
  );

  cone.applyMatrix4(RotationFromTo(new THREE.Vector3(0, 0, 1), direction));

  cone.position.add(vertex);
  return cone;
}

function CreatePoint(position: THREE.Vector3) {
  const geometry = new THREE.SphereGeometry(0.1, 32, 32);
  const material = new THREE.MeshBasicMaterial({
    color: 0x00ff00,
    wireframe: true,
  });

  return new THREE.Mesh(geometry, material);
}

const updateLabel = (
  pos: THREE.Object3D,
  label: HTMLDivElement,
  camera: THREE.Camera,
  canvas: HTMLCanvasElement
) => {
  pos.updateWorldMatrix(true, false);
  pos.getWorldPosition(tempV);

  camera ? tempV.project(camera) : null;

  const x = (tempV.x * 0.5 + 0.5) * canvas.clientWidth;
  const y = (tempV.y * -0.5 + 0.5) * canvas.clientHeight;
  label.style.transform = `translate(-50%, -50%) translate(${x}px,${y}px)`;
};

export { RotationFromTo, CreateCone, CreatePoint, updateLabel };
