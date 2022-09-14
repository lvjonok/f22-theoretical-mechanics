import {
  ArrowHelper,
  BufferGeometry,
  ColorRepresentation,
  Line,
  Vector3,
  Object3D,
  Float32BufferAttribute,
  LineBasicMaterial,
} from "three";

export class Vector extends Object3D {
  line: Line;

  constructor(
    public origin: Vector3,
    public end: Vector3,
    color?: ColorRepresentation
  ) {
    super();

    const lineGeometry = new BufferGeometry();
    lineGeometry.setAttribute(
      "position",
      new Float32BufferAttribute([0, 0, 0, 1, 1, 1], 3)
    );

    this.line = new Line(
      lineGeometry,
      new LineBasicMaterial({ color: color, toneMapped: false })
    );

    this.add(this.line);
  }

  setOrigin(origin: Vector3) {
    this.origin = origin;

    this.line.geometry.setAttribute(
      "position",
      new Float32BufferAttribute([origin.x, origin.y, origin.z, 1, 1, 1], 3)
    );
  }

  setEnd(end: Vector3) {
    this.end = end;

    this.line.geometry.setAttribute(
      "position",
      new Float32BufferAttribute(
        [this.origin.x, this.origin.y, this.origin.z, end.x, end.y, end.z],
        3
      )
    );
  }

  getWorldPosition(target: Vector3): Vector3 {
    target.set(this.end.x, this.end.y, this.end.z);
    return target;
  }
}
