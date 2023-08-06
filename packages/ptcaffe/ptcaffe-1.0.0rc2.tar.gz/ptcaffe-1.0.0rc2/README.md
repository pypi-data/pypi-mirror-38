## PTCaffe
PTCaffe is a caffe-like deep learning framework on pytorch, which implements the main logic of caffe. It supports network definition with prototxt and network training with solver file. 

The goal of ptcaffe consists of three aspects:
- maintain the compatibility between caffe and ptcaffe and expand new features
- maintain a set of model conversion tools between ptcaffe and other platforms
- make famous deep learning tasks work on ptcaffe

### [Installation](docs/doc/installation.md)
- Method1
```
pip install git+ssh://git@gitcv.ainirobot.com:10022/xiaohang/PytorchCaffe.git
```

- Method2
```
git clone ssh://git@gitcv.ainirobot.com:10022/xiaohang/PytorchCaffe.git
cd PytorchCaffe && make
```

### [Compatibility](docs/doc/compatibility.md)
- [x] python2.7
- [x] python3.6
- [x] pytorch0.4
- [ ] pytorch0.4.1
- [ ] pytorch1.0

### Document
see [document](docs/doc/document.md)

### Usage example
- train model
```
ptcaffe train --solver solver.prototxt --gpu 0 --verbose 1                           # train from begining
ptcaffe train --solver solver.prototxt --gpu 0 --verbose 1 --weights your.ptcmodel   # train with init weights
ptcaffe train --solver solver.prototxt --gpu 0 --verbose 1 --snapshot saved.ptcstate # resum training
```
set [verbose](docs/doc/verbose_level.md) large than 0 will output [receptive filed](docs/doc/receptive_field.md) of each layer

- test model
```
ptcaffe test --solver solver.prototxt --gpu 0 --weights saved.ptcmodel
```

- run model
```
ptcaffe run --model input.prototxt --gpu 0 --weights saved.ptcmodel --iterations 100
```

- [time model](docs/doc/time_model.md)
```
ptcaffe time --model input.prototxt --gpu 0 --iterations 100
```

- [fetch model](docs/doc/get_model.md)
```
ptcaffe get_model pytorch:resnet50       # fetch model from pytorch model zoo and convert to ptcaffe, works on pytorch0.3 only
ptcaffe get_model gluon:resnet50_v1      # fetch model from gluon model zoo and convert to ptcaffe
```

- [distributed train](demos/mnist_distributed): 
just set the following params in solover
```
distributed_backend:               # default nccl
distributed_master:                # master address
distributed_worldsize:             # machine number
distributed_rank:                  # rank id
```
Notice: For distributed training in python2.7, the multi processes dataloader is not supported. You can move to python3 to avoid this problem

- [multi\_tasks train](docs/doc/solver.md):
just set the following params in solover
```
selectors                          # task1,task2,...; the task list
selector_policy                    # ORDERED, RANDOM; the selector policy
test_iters                         # int,int,...; test_iter for each task
```
Besides the params setting in solver, you need to set selector param in corresponding task branch layers. See a [demo](demos/multi_tasks) here.

- model conversion<br><br>
  Ptcaffe contains many model conversion tools.  Each model conversion tool will first produce converted protofile and weightfile __automaticly__ and then verify the forward difference between two platforms. To make the verifying process works, please install the corresponding platform pacakge.
  - [x] [convert with caffe](demos/converter/caffe)
  <pre>
  caffe2ptcaffe input.prototxt input.caffemodel output.prototxt output.ptcmodel
  ptcaffe2caffe input.prototxt input.ptcmodel output.prototxt output.caffemodel
  </pre>
  - [x] [convert with darknet](demos/converter/darknet)
  <pre>
  darknet2ptcaffe input.cfg input.weights output.prototxt output.ptcmodel
  ptcaffe2darknet input.prototxt input.ptcmodel output.cfg output.weights
  cfg2prototxt input.cfg output.prototxt
  prototxt2cfg input.prototxt output.cfg
  </pre>
  - [ ] [convert with gluon](demos/converter/gluon)
  <pre>
  gluon2ptcaffe input.json input.params output.prototxt output.ptcmodel
  ptcaffe2gluon input.prototxt input.ptcmodel output.json output.params
  json2prototxt input.json output.prototxt
  prototxt2json input.prototxt output.json
  </pre>
  - [x] [convert from pytorch](demos/converter/pytorch)
  <pre>
  pytorch2ptcaffe input.prototxt input.ptcmodel output.prototxt output.ptcmodel
  </pre>
  currently works only on pytorch0.3 as onnx is conflict with pytorch0.4
  - [x] [convert with onnx](demos/converter/onnx)
  <pre>
  onnx2ptcaffe input.onnx output.prototxt output.ptcmodel
  ptcaffe2onnx input.prototxt input.ptcmodel output.onnx
  onnx2prototxt input.onnx output.prototxt
  </pre>
  there is no verification between onnx model and ptcaffe model
  - [ ] [convert with tensorflow](demos/converter/tensorflow)
  <pre>
  tensorflow2ptcaffe input.tf output.prototxt output.ptcmodel
  ptcaffe2tensorflow input.prototxt input.ptcmodel output.tf
  </pre>

- [other commands](demos/converter/other)
```
merge_bn input.prototxt input.ptcmodel output.prototxt output.ptcmodel
merge_bn input.prototxt output.prototxt
merge_scale input.prototxt input.ptcmodel output.prototxt output.ptcmodel
merge_scale input.prototxt output.prototxt
split_scale input.prototxt input.ptcmodel output.prototxt output.ptcmodel
split_scale input.prototxt output.prototxt
```

### Python Example
- Train model
<pre>
ptcaffe train --solver solver.prototxt --gpu 0
python train.py --solver solver.prototxt --gpu 0
</pre>
The above two commands are equivalent, where the train.py is defined as fellows.
<pre>
#file: train.py
import argparse
from ptcaffe.trainers import Trainer
</br>
parser = argparse.ArgumentParser(description='ptcaffe trainer')
parser.add_argument('--solver', help='the solver prototxt')
parser.add_argument('--weights', help='the pretrained weight')
parser.add_argument('--gpu', help='gpu ids e.g "0,1,2,3"')
</br>
args = parser.parse_args()
trainer = Trainer(args.solver, args.weights, args.gpu, args)
trainer.run()
</pre>
see [solver help](docs/doc/solver.md) and all [layers](docs/doc/layers.md) definition

- Forward network
<pre>
from ptcaffe.caffenet import CaffeNet
net = CaffeNet('resnet50.prototxt')
net.set_automatic_outputs()
net.load_model('resnet50.caffemodel')
net.eval()
</br>
img = cv2.imread(imgfile)
img = torch.from_numpy(img.transpose(2,0,1)).float().div(255.0).unsqueeze(0)
img = Variable(img)
blobs = net(img)
</pre>
see [CaffeNet API](docs/doc/caffenet.md)

- Add Layer
<br>To support new layer in train prototxt, you can easily add a new layer and register as fellows.
<pre>
from ptcaffe.layer_dict import register_layer<br>
@register_layer("LayerName")
class NewLayer(nn.Module):
&nbsp;&nbsp;def __init__(self, layer, *input_shapes):
&nbsp;&nbsp;&nbsp;&nbsp;super(self, NewLayer).__init__()
&nbsp;&nbsp;&nbsp;&nbsp;# init codes here <br>
&nbsp;&nbsp;def __repr__(self):
&nbsp;&nbsp;&nbsp;&nbsp;return "NewLayer()" <br>
&nbsp;&nbsp;def forward(self, *inputs):
&nbsp;&nbsp;&nbsp;&nbsp;# forward codes here<br>
&nbsp;&nbsp;def forward_shape(self, *input_shapes):
&nbsp;&nbsp;&nbsp;&nbsp;# forward shape code here
</pre>
see [details](docs/doc/add_layer.md) for more complex layer definition

### Train Results

Name | caffe | pytorch | ptcaffe | script | download
:---:|:-----:|:-------:|:-------:|:------:|:--------:
imagenet-resnet50 | [75.3%/92.2%](https://github.com/KaimingHe/deep-residual-networks) | - | 76.15%/92.88% | [script](examples/imagenet/resnet50) | [weight](https://pan.baidu.com/s/1Ja_FxMyoHtGio0R6qYJ62g) [log](https://pan.baidu.com/s/11D7qo-xe-EBJNWOKPNvpoA) 
imagenet-peleenet | 71.3%/90.3% | - | 70.45%/89.82% | [script](examples/imagenet/peleenet) | [weight](https://pan.baidu.com/s/18KIYffsGCmHGCuJp2LPc6w) | [log](https://pan.baidu.com/s/1LMk1x8SL2UW6U1O7AELUCw)
imagenet-mobilenetv2 | [71.9%/90.49%](https://github.com/shicai/MobileNet-Caffe) | - | 71.03%/90.06% | [script](examples/imagenet/mobilenetv2) | [weight](https://pan.baidu.com/s/19Bi71iuqh5CHmyrDRgjKCg) | [log](https://pan.baidu.com/s/1I5kwP5AfEL_DNqtNHZqTwA)
ssd_voc_vgg16 | [77.2%](https://github.com/weiliu89/caffe/tree/ssd) | - | 77.37% | [script](examples/ssd/vgg16_voc_list) | [weight](https://pan.baidu.com/s/1SMda-Xtsb1If7nEHb4PhEA) [log](https://pan.baidu.com/s/19mLVOQQSsGz94WMQtv5HQA)
ssd_voc_RFBSSD | - | - | - | - | -
ssd_voc_MobilenetV2 | - | - | - | - | -
frcnn_voc_vgg16 | - | [70.1%](https://github.com/jwyang/faster-rcnn.pytorch) | 71.82% | [script](examples/faster-rcnn/frcnn_voc_vgg16) | - | -
rfcn_voc_resnet50_ohem | [-](https://github.com/YuwenXiong/py-R-FCN) | - | 76.1% | [script](examples/rfcn/rfcn_voc_resnet50_ohem) | [weight](https://pan.baidu.com/s/1SGY0is20MLF69LLA93h7rw) [log](https://pan.baidu.com/s/1ePjYKTErhRkh5f54uvWJ8A)
yolov2_voc | - | - | 72.34% | [script](examples/yolo/yolov2_voc) | - | -
fcn_fcn8satonce | 65.40% | [64.74%](https://github.com/wkentaro/pytorch-fcn) | 65.23% | [script](examples/fcn/fcn8s_atonce) | [weight](https://pan.baidu.com/s/1fuyXOU1ZnGI8zwz7mYYs_w) [log](https://pan.baidu.com/s/1YHO1iv2CjnfIbjTaSWcZiw)
fcn_fcn32s | 63.63% | [62.84%](https://github.com/wkentaro/pytorch-fcn) | 63.57% | [script](examples/fcn/fcn32s) | [weight](https://pan.baidu.com/s/1sZ6-3ghkOpYjBybf7DZy1w) [log](https://pan.baidu.com/s/1dxazaD3ya19wZGZMxc2OvA)
deeplabv3_resnet101 | - | 79.19% | 79.29% | [script](examples/deeplab/deeplab_v3/train_vocdata_nesterov.prototxt) | [weight](https://pan.baidu.com/s/1SevI8IE9P73Edd3dm8UOhw) [log](https://pan.baidu.com/s/17sCwDuRCJly7Qt4uqDwQmg)
openpose | - | - | - | - | -
widerface_SFD | 93.5/92.1/85.8 | - | 94.1/92.7/84.9 | [script](examples/widerface/SFD) | [weight](https://pan.baidu.com/s/1SrU8Xp0opTnETprRb0A1Xw) | -
OCR_EAST | - | - | - | - | -


### FAQ
- Is there incompitible between caffe and ptcaffe?
  - the bias_term of Scale layer in caffe is default False, but True in ptcaffe
  - ScoreEvaluator in fcn plugin, ptcaffe change num_class -> num_classes
  - mean values in ImageData should be quoted

- How to make training results deterministic?
  - set manual seed in solver
  - set CUDNN_DETERMINISTIC true in solver
  - set num_workers to 0
