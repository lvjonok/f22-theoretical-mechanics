import * as THREE from "three";
import { MathUtils } from "three";
import { RotationFromTo } from "./vis";

// define constants from task description
export const OM0 = 40.0;
export const alphaB = 120.0;
export const alphaA = 30.0;
export const w1 = 2;
export const e1 = 3.7;
export const M0M = 5.0;
export const phi0 = 0;

// function mapping time of the simulation to phi angle of the cone (angle of cone A around Z axis)
function timeToPhi(time: number) {
  return phi0 + w1 * time + (e1 * time * time) / 2;
}

export const coneAstartAxis = new THREE.Vector3(
  0,
  -Math.cos(Math.PI / 4),
  -Math.sin(Math.PI / 4)
);
export const coneAradiusAxis = new THREE.Vector3(
  0,
  -Math.cos(Math.PI / 4),
  Math.sin(Math.PI / 4)
);

export const startingICAxis = new THREE.Vector3(
  0,
  Math.sin(MathUtils.degToRad(alphaB / 2)),
  Math.cos(MathUtils.degToRad(alphaB / 2))
);

export default class Model {
  prev?: Model;

  timestamp: number;
  phi: number;
  axisA: THREE.Vector3;
  axisIC: THREE.Vector3;
  centerA: THREE.Vector3;
  thetaA: number;

  // parameters we want to find in the simulation
  angVelA: THREE.Vector3;
  angAccA: THREE.Vector3;

  posM: THREE.Vector3;
  velM: THREE.Vector3;
  accM: THREE.Vector3;

  constructor(timestamp: number, prev?: Model) {
    this.timestamp = timestamp;

    this.phi = timeToPhi(timestamp);
    this.prev = prev;

    this.axisA = coneAstartAxis
      .clone()
      .applyAxisAngle(new THREE.Vector3(0, 0, 1), this.phi);
    this.centerA = this.axisA
      .clone()
      .multiplyScalar(-OM0 * Math.cos(MathUtils.degToRad(alphaA / 2)));
    console.log("length of centerA", this.centerA.length());
    this.thetaA =
      (this.phi * OM0) / (OM0 * Math.sin(MathUtils.degToRad(alphaA / 2.0)));
    // calculate transformation for base of the rolling cone A
    const rad = coneAradiusAxis
      .clone()
      .applyAxisAngle(new THREE.Vector3(0, 0, 1), this.phi)
      .applyAxisAngle(this.axisA, this.thetaA);
    const shift = rad
      .clone()
      .normalize()
      .multiplyScalar(OM0 * Math.sin(MathUtils.degToRad(alphaA / 2.0)) - M0M);
    const posM = this.centerA.clone().add(shift);
    this.posM = posM;
    this.velM = this.prev
      ? this.posM
          .clone()
          .sub(this.prev.posM)
          .multiplyScalar(1 / (this.timestamp - this.prev.timestamp))
      : new THREE.Vector3(0, 0, 0);
    this.accM = this.prev
      ? this.velM
          .clone()
          .sub(this.prev.velM)
          .multiplyScalar(1 / (this.timestamp - this.prev.timestamp))
      : new THREE.Vector3(0, 0, 0);

    this.angAccA = new THREE.Vector3();

    const velCenterA = this.prev
      ? this.centerA
          .clone()
          .sub(this.prev.centerA)
          .multiplyScalar(1 / (this.timestamp - this.prev.timestamp))
      : new THREE.Vector3();

    this.axisIC = startingICAxis
      .clone()
      .applyAxisAngle(new THREE.Vector3(0, 0, 1), this.phi)
      .normalize()
      .multiplyScalar(OM0);

    const radIC = this.centerA.clone().sub(this.axisIC.clone());

    this.angVelA = radIC
      .clone()
      .cross(velCenterA.clone())
      .divideScalar(radIC.dot(radIC));

    this.angAccA = this.prev
      ? this.angVelA
          .clone()
          .sub(this.prev.angVelA)
          .multiplyScalar(1 / (this.timestamp - this.prev.timestamp))
      : new THREE.Vector3();
  }
}
