import numpy

model = numpy.zeros([3301, 201], dtype=numpy.float32)

model[:, :] = 1500.0

for i in range(3301):
    for k in range(10, 201):
        if ((i - 1500)**2 + (k - 100)**2 < 2000):
            model[i, k] = 4500.0
        else:
            model[i, k] = model[i, k] + 15 * k

model = numpy.transpose(model)

# model.tofile('circ2D-TrueVp_rough.bin', sep='')
