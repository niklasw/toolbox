// STAR-CCM+ macro: t.java
package myFunctions;

import star.base.neo.*;

public class myOps {

	public myOps() {
	}

	public DoubleVector crossProduct(DoubleVector v1, DoubleVector v2) {
		double r0 = v1.getComponent(1) * v2.getComponent(2)
			- v1.getComponent(2) * v2.getComponent(1);
		double r1 = -(v1.getComponent(0) * v2.getComponent(2)
			- v1.getComponent(2) * v2.getComponent(0));
		double r2 = v1.getComponent(0) * v2.getComponent(1)
			- v1.getComponent(1) * v2.getComponent(0);

		DoubleVector r = new DoubleVector(new double[]{r0, r1, r2});
		return r;
	}

	public double dotProduct(DoubleVector v1, DoubleVector v2) {
		return v1.getComponent(0) * v2.getComponent(0)
			+ v1.getComponent(1) * v2.getComponent(1)
			+ v1.getComponent(2) * v2.getComponent(2);
	}

	public DoubleVector normalize(DoubleVector t) {
		double length = Math.sqrt(dotProduct(t, t));
		t.setComponent(0, t.getComponent(0) / length);
		t.setComponent(1, t.getComponent(1) / length);
		t.setComponent(2, t.getComponent(2) / length);
		return t;
	}

	public DoubleVector tangentVector(DoubleVector planeNormal) {
		DoubleVector random = normalize(new DoubleVector(new double[]{0, 1, 0}));
		while (dotProduct(random, planeNormal) > 0.5) {
			random = normalize(new DoubleVector(new double[]{Math.random(), Math.random(), Math.random()}));
			System.out.println("Random vector" + random);
		}
		DoubleVector t = crossProduct(planeNormal, random);
		t = normalize(t);
		return t;
	}

	public DoubleVector scalarMultiply(DoubleVector v, Double d) {
		return new DoubleVector(new double[]{
				v.getComponent(0) * d,
				v.getComponent(1) * d,
				v.getComponent(2) * d});
	}

	public DoubleVector vectorAddition(DoubleVector v1, DoubleVector v2) {
		return new DoubleVector(new double[]{
				v1.getComponent(0) + v2.getComponent(0),
				v1.getComponent(1) + v2.getComponent(1),
				v1.getComponent(2) + v2.getComponent(2)});
	}
}
