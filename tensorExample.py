import torch

dtype = torch.float
device = torch.device("cpu")
# device = torch.device("cuda:0")

batch_size, D_in, hidden_size, D_out = 64, 1000, 100, 10

x = torch.randn(batch_size, D_in, device=device, dtype=dtype)
y = torch.randn(batch_size, D_out, device=device, dtype=dtype)

w1 = torch.randn(D_in, hidden_size, device=device, dtype=dtype)
w2 = torch.randn(hidden_size, D_out, device=device, dtype=dtype)

learning_rate = 1e-6

for t in range(500):
    h = x.mm(w1)
    h_relu = h.clamp(min=0)
    y_pred = h_relu.mm(w2)

    loss = (y_pred - y).pow(2).sum().item()
    print(t, loss)

    # Back propagation
    grad_y_pred = 2.0 * (y_pred - y)
    grad_w2 = h_relu.t().mm(grad_y_pred)
    grad_h_relu = grad_y_pred.mm(w2.t())
    grad_h = grad_h_relu.clone()
    grad_h[h < 0] = 0

    grad_w1 = x.t().mm(grad_h)

    w1 -= learning_rate * grad_w1
    w2 -= learning_rate * grad_w2
