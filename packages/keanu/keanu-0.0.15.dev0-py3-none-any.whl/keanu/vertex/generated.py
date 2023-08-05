## This is a generated file. DO NOT EDIT.

from py4j.java_gateway import java_import
from keanu.context import KeanuContext
from .base import Vertex

context = KeanuContext()


java_import(context.jvm_view(), "io.improbable.keanu.vertices.bool.nonprobabilistic.ConstantBoolVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.bool.nonprobabilistic.operators.binary.compare.EqualsVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.bool.nonprobabilistic.operators.binary.compare.GreaterThanOrEqualVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.bool.nonprobabilistic.operators.binary.compare.GreaterThanVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.bool.nonprobabilistic.operators.binary.compare.LessThanOrEqualVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.bool.nonprobabilistic.operators.binary.compare.LessThanVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.bool.nonprobabilistic.operators.binary.compare.NotEqualsVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.nonprobabilistic.CastDoubleVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.nonprobabilistic.ConstantDoubleVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.nonprobabilistic.DoubleIfVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.nonprobabilistic.operators.binary.AdditionVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.nonprobabilistic.operators.binary.DifferenceVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.nonprobabilistic.operators.binary.DivisionVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.nonprobabilistic.operators.binary.MultiplicationVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.nonprobabilistic.operators.binary.PowerVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.nonprobabilistic.operators.unary.AbsVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.nonprobabilistic.operators.unary.CeilVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.nonprobabilistic.operators.unary.FloorVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.nonprobabilistic.operators.unary.RoundVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.probabilistic.CauchyVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.probabilistic.ExponentialVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.probabilistic.GammaVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.probabilistic.GaussianVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.dbl.probabilistic.UniformVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.intgr.nonprobabilistic.ConstantIntegerVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.intgr.nonprobabilistic.operators.binary.IntegerDivisionVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.intgr.probabilistic.PoissonVertex")
java_import(context.jvm_view(), "io.improbable.keanu.vertices.intgr.probabilistic.UniformIntVertex")


def ConstantBool(constant) -> context.jvm_view().ConstantBoolVertex:
    return Vertex(context.jvm_view().ConstantBoolVertex, constant)


def Equals(a, b) -> context.jvm_view().EqualsVertex:
    return Vertex(context.jvm_view().EqualsVertex, a, b)


def GreaterThanOrEqual(a, b) -> context.jvm_view().GreaterThanOrEqualVertex:
    return Vertex(context.jvm_view().GreaterThanOrEqualVertex, a, b)


def GreaterThan(a, b) -> context.jvm_view().GreaterThanVertex:
    return Vertex(context.jvm_view().GreaterThanVertex, a, b)


def LessThanOrEqual(a, b) -> context.jvm_view().LessThanOrEqualVertex:
    return Vertex(context.jvm_view().LessThanOrEqualVertex, a, b)


def LessThan(a, b) -> context.jvm_view().LessThanVertex:
    return Vertex(context.jvm_view().LessThanVertex, a, b)


def NotEquals(a, b) -> context.jvm_view().NotEqualsVertex:
    return Vertex(context.jvm_view().NotEqualsVertex, a, b)


def CastDouble(input_vertex) -> context.jvm_view().CastDoubleVertex:
    return Vertex(context.jvm_view().CastDoubleVertex, input_vertex)


def ConstantDouble(constant) -> context.jvm_view().ConstantDoubleVertex:
    return Vertex(context.jvm_view().ConstantDoubleVertex, constant)


def DoubleIf(shape, predicate, thn, els) -> context.jvm_view().DoubleIfVertex:
    return Vertex(context.jvm_view().DoubleIfVertex, shape, predicate, thn, els)


def Addition(left, right) -> context.jvm_view().AdditionVertex:
    return Vertex(context.jvm_view().AdditionVertex, left, right)


def Difference(left, right) -> context.jvm_view().DifferenceVertex:
    return Vertex(context.jvm_view().DifferenceVertex, left, right)


def Division(left, right) -> context.jvm_view().DivisionVertex:
    return Vertex(context.jvm_view().DivisionVertex, left, right)


def Multiplication(left, right) -> context.jvm_view().MultiplicationVertex:
    return Vertex(context.jvm_view().MultiplicationVertex, left, right)


def Power(base, exponent) -> context.jvm_view().PowerVertex:
    return Vertex(context.jvm_view().PowerVertex, base, exponent)


def Abs(input_vertex) -> context.jvm_view().AbsVertex:
    return Vertex(context.jvm_view().AbsVertex, input_vertex)


def Ceil(input_vertex) -> context.jvm_view().CeilVertex:
    return Vertex(context.jvm_view().CeilVertex, input_vertex)


def Floor(input_vertex) -> context.jvm_view().FloorVertex:
    return Vertex(context.jvm_view().FloorVertex, input_vertex)


def Round(input_vertex) -> context.jvm_view().RoundVertex:
    return Vertex(context.jvm_view().RoundVertex, input_vertex)


def Cauchy(location, scale) -> context.jvm_view().CauchyVertex:
    return Vertex(context.jvm_view().CauchyVertex, location, scale)


def Exponential(rate) -> context.jvm_view().ExponentialVertex:
    return Vertex(context.jvm_view().ExponentialVertex, rate)


def Gamma(theta, k) -> context.jvm_view().GammaVertex:
    return Vertex(context.jvm_view().GammaVertex, theta, k)


def Gaussian(mu, sigma) -> context.jvm_view().GaussianVertex:
    return Vertex(context.jvm_view().GaussianVertex, mu, sigma)


def Uniform(x_min, x_max) -> context.jvm_view().UniformVertex:
    return Vertex(context.jvm_view().UniformVertex, x_min, x_max)


def ConstantInteger(constant) -> context.jvm_view().ConstantIntegerVertex:
    return Vertex(context.jvm_view().ConstantIntegerVertex, constant)


def IntegerDivision(a, b) -> context.jvm_view().IntegerDivisionVertex:
    return Vertex(context.jvm_view().IntegerDivisionVertex, a, b)


def Poisson(mu) -> context.jvm_view().PoissonVertex:
    return Vertex(context.jvm_view().PoissonVertex, mu)


def UniformInt(min, max) -> context.jvm_view().UniformIntVertex:
    return Vertex(context.jvm_view().UniformIntVertex, min, max)
