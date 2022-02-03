import numpy as np
x = np.array([1,2,3])
w = np.array([4,5,6])
y = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,9]
])
z = np.array([
    [2,3,4],
    [5,6,7],
    [8,9,1]
])


print('x dim', x.ndim)
print('x shape', x.shape)
print('x size', x.size)
print('x type', x.dtype)

print('y dim', y.ndim)
print('y shape', y.shape)
print('y size', y.size)
print('y type', y.dtype)

print('x + w', x + w)
print('x * w', x * w)

print(np.dot(x, z))
#print(y.shape)
#print(y.ndim)

#数学関数
print('pi', np.pi)
print('e', np.e)
print('log(x)', np.log(x))

#要素の読み取り
print('x[2]', x[2])
print('x[1:]', x[1:])
print('y[0,1]', y[0,1])
print('y[1, :]', y[1,:])

#初期化
xx = np.random.randint(0,10, (3,3))
print('xx', xx)

