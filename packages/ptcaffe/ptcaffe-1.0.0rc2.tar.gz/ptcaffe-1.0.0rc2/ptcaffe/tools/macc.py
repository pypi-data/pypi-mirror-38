import numpy
import os
import ptcaffe.caffenet as caffenet
import sys


def MACC(protofile):
    cn = caffenet.CaffeNet(protofile)
    input_shape = cn.get_input_shapes()
    featuremap_shape = {'data': [None, input_shape, None]}
    layers = cn.net_info['layers']

    for layer in layers:
        lname = layer['name']
        input_shape = [0, 0]

        if layer['type'] == "Concat":
            flag = 0
            for layer_bottom in layer['bottom']:
                if 0 == flag:
                    input_shape = featuremap_shape[layer_bottom][1]
                    flag = 1
                else:
                    input_shape[1] = input_shape[1] + featuremap_shape[layer_bottom][1][1]
        elif layer['type'] == "Scale" and type(layer['bottom']) == type([1, ]):
            input_shape = (featuremap_shape[layer['bottom'][0]][1])
        else:
            if type(layer['bottom']) == type([1, ]):
                input_shape = (featuremap_shape[layer['bottom'][0]][1])
            else:
                input_shape = (featuremap_shape[layer['bottom']][1])

        try:
            output_shape = cn.models[lname].forward_shape(input_shape)
        except IndexError as e:
            print(e)
            print(lname, ',', protofile)
            print("input_shape:", input_shape)
            exit(0)
        featuremap_shape[lname] = [input_shape, output_shape, layer['type']]

    conv_sums = 0
    ip_sums = 0
    for name in featuremap_shape:
        in_out = featuremap_shape[name]
        if featuremap_shape[name][2] == 'Convolution':
            kernel_size = cn.models[name].weight.shape
            conv_sums = conv_sums + in_out[0][1] * kernel_size[2] * kernel_size[3] * in_out[1][1] * in_out[1][2] * in_out[1][3]
        if featuremap_shape[name][2] == 'InnerProduct':
            kernel_size = cn.models[name].weight.shape
            ip_sums = ip_sums + kernel_size[0] * kernel_size[1]
    sumups = conv_sums + ip_sums
    return sumups, conv_sums, ip_sums


if __name__ == '__main__':
    import pandas
    filepath = './prototxt/'
    files = os.listdir(filepath)
    file_name = []
    time = []
    for file in files:
        time.append(MACC(filepath+file))
        file_name.append(file.split('.')[0])
    file_time = pandas.DataFrame(data={'net': file_name, 'MACC': time})
    file_time.to_csv('time.csv')
