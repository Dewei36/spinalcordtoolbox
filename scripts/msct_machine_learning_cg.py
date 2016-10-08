#!/usr/bin/env python
#########################################################################################
#
# This module contains some functions and classes for patch-based machine learning
#
# ---------------------------------------------------------------------------------------
# Copyright (c) 2016 Polytechnique Montreal <www.neuro.polymtl.ca>
# Authors: Benjamin De Leener
# Modified: 2016-10-04
#
# About the license: see the file LICENSE.TXT
#########################################################################################

import os
import sct_utils as sct
from msct_image import Image
import numpy as np
import itertools
import json
import pickle
from progressbar import Bar, ETA, Percentage, ProgressBar, Timer
from skimage.feature import hog

def extract_patches_from_image(path_dataset, fname_raw_images, fname_gold_images, patches_coordinates, patch_info, verbose=1):
    # input: list_raw_images
    # input: list_gold_images
    # output: list of patches. One patch is a pile of patches from (first) raw images and (second) gold images. Order are respected.

    # TODO: apply rotation of the image to take patches in planes event when doing the extraction in physical space

    patch_size = patch_info['patch_size']  # [int, int]
    patch_pixdim = patch_info['patch_pixdim']  # {'axial': [float, float], 'sagittal': [float, float], 'frontal': [float, float]}

    raw_images = [Image(path_dataset + fname) for fname in fname_raw_images]
    gold_images = [Image(path_dataset + fname) for fname in fname_gold_images]

    for k in range(len(patches_coordinates)):

        ind = [patches_coordinates[k][0], patches_coordinates[k][1], patches_coordinates[k][2]]
        patches_raw, patches_gold = [], []

        if 'axial' in patch_pixdim:
            range_x = np.linspace(ind[0] - (patch_size[0] / 2.0) * patch_pixdim['axial'][0], ind[0] + (patch_size[0] / 2.0) * patch_pixdim['axial'][0], patch_size[0])
            range_y = np.linspace(ind[1] - (patch_size[1] / 2.0) * patch_pixdim['axial'][1], ind[1] + (patch_size[1] / 2.0) * patch_pixdim['axial'][1], patch_size[1])
            coord_x, coord_y = np.meshgrid(range_x, range_y)
            coord_x = coord_x.ravel()
            coord_y = coord_y.ravel()
            coord_physical = [[coord_x[i], coord_y[i], ind[2]] for i in range(len(coord_x))]

            for raw_image in raw_images:
                grid_voxel = np.array(raw_image.transfo_phys2continuouspix(coord_physical))
                patch = np.reshape(raw_image.get_values(np.array([grid_voxel[:, 0], grid_voxel[:, 1], grid_voxel[:, 2]]),
                                                        interpolation_mode=1), (patch_size[0], patch_size[1]))
                patches_raw.append(np.expand_dims(patch, axis=0))

            for gold_image in gold_images:
                grid_voxel = np.array(gold_image.transfo_phys2continuouspix(coord_physical))
                patch = np.reshape(gold_image.get_values(np.array([grid_voxel[:, 0], grid_voxel[:, 1], grid_voxel[:, 2]]),
                                                         interpolation_mode=0), (patch_size[0], patch_size[1]))
                patches_gold.append(np.expand_dims(patch, axis=0))

        if 'sagittal' in patch_pixdim:
            range_x = np.linspace(ind[0] - (patch_size[0] / 2.0) * patch_pixdim['sagittal'][0], ind[0] + (patch_size[0] / 2.0) * patch_pixdim['sagittal'][0], patch_size[0])
            range_y = np.linspace(ind[1] - (patch_size[1] / 2.0) * patch_pixdim['sagittal'][1], ind[1] + (patch_size[1] / 2.0) * patch_pixdim['sagittal'][1], patch_size[1])
            coord_x, coord_y = np.meshgrid(range_x, range_y)
            coord_x = coord_x.ravel()
            coord_y = coord_y.ravel()
            coord_physical = [[ind[0], coord_x[i], coord_y[i]] for i in range(len(coord_x))]

            for raw_image in raw_images:
                grid_voxel = np.array(raw_image.transfo_phys2continuouspix(coord_physical))
                patch = np.reshape(raw_image.get_values(np.array([grid_voxel[:, 0], grid_voxel[:, 1], grid_voxel[:, 2]]),
                                                        interpolation_mode=1), (patch_size[0], patch_size[1]))
                patches_raw.append(np.expand_dims(patch, axis=0))

            for gold_image in gold_images:
                grid_voxel = np.array(gold_image.transfo_phys2continuouspix(coord_physical))
                patch = np.reshape(gold_image.get_values(np.array([grid_voxel[:, 0], grid_voxel[:, 1], grid_voxel[:, 2]]),
                                                         interpolation_mode=0), (patch_size[0], patch_size[1]))
                patches_gold.append(np.expand_dims(patch, axis=0))

        if 'frontal' in patch_pixdim:
            range_x = np.linspace(ind[0] - (patch_size[0] / 2.0) * patch_pixdim['frontal'][0], ind[0] + (patch_size[0] / 2.0) * patch_pixdim['frontal'][0], patch_size[0])
            range_y = np.linspace(ind[1] - (patch_size[1] / 2.0) * patch_pixdim['frontal'][1], ind[1] + (patch_size[1] / 2.0) * patch_pixdim['frontal'][1], patch_size[1])
            coord_x, coord_y = np.meshgrid(range_x, range_y)
            coord_x = coord_x.ravel()
            coord_y = coord_y.ravel()
            coord_physical = [[coord_x[i], ind[1], coord_y[i]] for i in range(len(coord_x))]

            for raw_image in raw_images:
                grid_voxel = np.array(raw_image.transfo_phys2continuouspix(coord_physical))
                patch = np.reshape(raw_image.get_values(np.array([grid_voxel[:, 0], grid_voxel[:, 1], grid_voxel[:, 2]]),
                                                        interpolation_mode=1), (patch_size[0], patch_size[1]))
                patches_raw.append(np.expand_dims(patch, axis=0))

            for gold_image in gold_images:
                grid_voxel = np.array(gold_image.transfo_phys2continuouspix(coord_physical))
                patch = np.reshape(gold_image.get_values(np.array([grid_voxel[:, 0], grid_voxel[:, 1], grid_voxel[:, 2]]),
                                                         interpolation_mode=0), (patch_size[0], patch_size[1]))
                patches_gold.append(np.expand_dims(patch, axis=0))

        patches_raw = np.concatenate(patches_raw, axis=0)
        patches_gold = np.concatenate(patches_gold, axis=0)

        yield {'patches_raw': patches_raw, 'patches_gold': patches_gold}


def get_minibatch(patch_iter, size):
    """Extract a minibatch of examples, return a tuple X_text, y.

    Note: size is before excluding invalid docs with no topics assigned.

    """
    data = [(patch['patches_raw'], patch['patches_gold']) for patch in itertools.islice(patch_iter, size)]

    if not len(data):
        return {'patches_raw': np.asarray([], dtype=np.float), 'patches_gold': np.asarray([], dtype=np.float)}

    patches_raw, patches_gold = zip(*data)
    patches_raw, patches_gold = np.asarray(patches_raw, dtype=np.float), np.asarray(patches_gold, dtype=np.float)

    return {'patches_raw': patches_raw, 'patches_gold': patches_gold}

class FileManager():
    def __init__(self, dataset_path, fct_explore_dataset, patch_extraction_parameters, fct_groundtruth_patch):
        self.dataset_path = sct.slash_at_the_end(dataset_path, slash=1)
        # This function should take the path to the dataset as input and outputs the list of files (wrt dataset path) that compose the dataset (image + groundtruth)
        self.fct_explore_dataset = fct_explore_dataset

        self.patch_extraction_parameters = patch_extraction_parameters
        # ratio_dataset represents the ratio between the training, testing and validation datasets.
        # default is: 60% training, 20% testing, 20% validation
        if 'ratio_dataset' in self.patch_extraction_parameters:
            self.ratio_dataset = self.patch_extraction_parameters['ratio_dataset']
        else:
            self.ratio_dataset = [0.6, 0.2, 0.2]
        # patch size is the number of pixels that are in a patch in each dimensions. Patches are only 2D
        # warning: patch size must correspond to the ClassificationModel
        # Example: [32, 32] means a patch with 32x32 pixels
        if 'patch_size' in self.patch_extraction_parameters:
            self.patch_size = self.patch_extraction_parameters['patch_size']
        else:
            self.patch_size = None
        # patch_pixdim represents the resolution of the patch
        if 'patch_pixdim' in self.patch_extraction_parameters:
            self.patch_pixdim = self.patch_extraction_parameters['patch_pixdim']
        else:
            self.patch_pixdim = None
        # extract_all_positive is a boolean variable. If True, the system extracts all positive patches from the dataset
        if 'extract_all_positive' in self.patch_extraction_parameters:
            self.extract_all_positive = self.patch_extraction_parameters['extract_all_positive']
        else:
            self.extract_all_positive = False
        # extract_all_negative is a boolean variable. If True, the system extracts all positive patches from the dataset
        if 'extract_all_negative' in self.patch_extraction_parameters:
            self.extract_all_negative = self.patch_extraction_parameters['extract_all_negative']
        else:
            self.extract_all_negative = False
        # ratio_patches_voxels is the ratio of patches to extract in all the possible patches in the images. Typically = 10%
        if 'ratio_patches_voxels' in self.patch_extraction_parameters:
            self.ratio_patches_voxels = self.patch_extraction_parameters['ratio_patches_voxels']
        else:
            self.ratio_patches_voxels = 0.1
        if 'batch_size' in self.patch_extraction_parameters:
            self.batch_size = self.patch_extraction_parameters['batch_size']
        else:
            self.batch_size = 1

        # patch_info is the structure that will be transmitted for patches extraction
        self.patch_info = {'patch_size': self.patch_size, 'patch_pixdim': self.patch_pixdim}

        # this function will be called on each patch to know its class/label
        self.fct_groundtruth_patch = fct_groundtruth_patch

        self.list_files = np.array(self.fct_explore_dataset(self.dataset_path))
        self.number_of_images = len(self.list_files)

        self.training_dataset, self.testing_dataset = [], []

        # list_classes is a dictionary that contains all the classes that are present in the dataset
        # this list is filled up iteratively while exploring the dataset
        # the key is the label of the class and the element is the number of element of each class
        self.list_classes = {}

        # class_weights is a dictionary containing the ratio of each class and the most represented class
        # len(class_weights) = len(list_classes)
        self.class_weights = {}

    def decompose_dataset(self, path_output):
        array_indexes = range(self.number_of_images)
        np.random.shuffle(array_indexes)

        self.training_dataset = self.list_files[np.ix_(array_indexes[:int(self.ratio_dataset[0] * self.number_of_images)])]
        self.testing_dataset = self.list_files[np.ix_(array_indexes[int(self.ratio_dataset[0] * self.number_of_images):int(self.ratio_dataset[0] * self.number_of_images)
                                                                                            +int(self.ratio_dataset[1] * self.number_of_images)])]

        results = {
            'training': {'raw_images': [data[0].tolist() for data in self.training_dataset], 'gold_images': [data[1].tolist() for data in self.training_dataset]},
            'testing': {'raw_images': [data[0].tolist() for data in self.testing_dataset], 'gold_images': [data[1].tolist() for data in self.testing_dataset]},
            'dataset_path': self.dataset_path
        }
        with open(path_output + 'datasets.json', 'w') as outfile:
            json.dump(results, outfile)

        return self.training_dataset, self.testing_dataset

    def iter_minibatches(self, patch_iter, minibatch_size):
        """Generator of minibatches."""
        data = get_minibatch(patch_iter, minibatch_size)
        while len(data['patches_raw']):
            yield data
            data = get_minibatch(patch_iter, minibatch_size)

    def compute_patches_coordinates(self, image):
        if self.extract_all_negative or self.extract_all_positive:
            print 'Extract all negative/positive patches: feature not yet ready...'

        image_dim = image.dim

        x, y, z = np.mgrid[0:image_dim[0], 0:image_dim[1], 0:image_dim[2]]
        indexes = np.array(zip(x.ravel(), y.ravel(), z.ravel()))
        physical_coordinates = np.asarray(image.transfo_pix2phys(indexes))

        random_batch = np.random.choice(physical_coordinates.shape[0], int(round(physical_coordinates.shape[0] * self.ratio_patches_voxels)))

        return physical_coordinates[random_batch]

    def explore(self):
        # training dataset
        global_results_patches = {'patch_info': self.patch_info}

        # TRAINING DATASET
        results_training = {}
        classes_training = {}
        for i, fnames in enumerate(self.training_dataset):
            fname_raw_images = self.training_dataset[i][0]
            fname_gold_images = self.training_dataset[i][1]
            reference_image = Image(self.dataset_path + fname_raw_images[0])  # first raw image is selected as reference

            patches_coordinates = self.compute_patches_coordinates(reference_image)
            print 'Number of patches in ' + fname_raw_images[0] + ' = ' + str(patches_coordinates.shape[0])

            stream_data = extract_patches_from_image(path_dataset=self.dataset_path,
                                                     fname_raw_images=fname_raw_images,
                                                     fname_gold_images=fname_gold_images,
                                                     patches_coordinates=patches_coordinates,
                                                     patch_info=self.patch_info,
                                                     verbose=1)

            minibatch_iterator_test = self.iter_minibatches(stream_data, self.batch_size)
            labels = []
            pbar = ProgressBar(widgets=[
                Timer(),
                ' ', Percentage(),
                ' ', Bar(),
                ' ', ETA()], max_value=patches_coordinates.shape[0])
            pbar.start()
            number_done = 0
            for data in minibatch_iterator_test:
                if np.ndim(data['patches_gold']) == 4:
                    labels.extend(center_of_patch_equal_one(data))
                    number_done += data['patches_gold'].shape[0]
                    pbar.update(number_done)
            pbar.finish()

            classes_in_image, counts = np.unique(labels, return_counts=True)
            for j, cl in enumerate(classes_in_image):
                if str(cl) not in classes_training:
                    classes_training[str(cl)] = [counts[j], 0.0]
                else:
                    classes_training[str(cl)][0] += counts[j]

            results_training[str(i)] = [[patches_coordinates[j, :].tolist(), labels[j]] for j in range(len(labels))]

        global_results_patches['training'] = results_training

        count_max_class, max_class = 0, ''
        for cl in classes_training:
            if classes_training[cl][0] > count_max_class:
                max_class = cl
        for cl in classes_training:
            classes_training[cl][1] = classes_training[cl][0] / float(classes_training[max_class][0])


        # TESTING DATASET
        results_testing = {}
        classes_testing = {}
        for i, fnames in enumerate(self.testing_dataset):
            fname_raw_images = self.testing_dataset[i][0]
            fname_gold_images = self.testing_dataset[i][1]
            reference_image = Image(self.dataset_path + fname_raw_images[0])  # first raw image is selected as reference

            patches_coordinates = self.compute_patches_coordinates(reference_image)
            print 'Number of patches in ' + fname_raw_images[0] + ' = ' + str(patches_coordinates.shape[0])

            stream_data = extract_patches_from_image(path_dataset=self.dataset_path,
                                                     fname_raw_images=fname_raw_images,
                                                     fname_gold_images=fname_gold_images,
                                                     patches_coordinates=patches_coordinates,
                                                     patch_info=self.patch_info,
                                                     verbose=1)

            minibatch_iterator_test = self.iter_minibatches(stream_data, self.batch_size)
            labels = []
            pbar = ProgressBar(widgets=[
                Timer(),
                ' ', Percentage(),
                ' ', Bar(),
                ' ', ETA()], max_value=patches_coordinates.shape[0])
            pbar.start()
            number_done = 0
            for data in minibatch_iterator_test:
                if np.ndim(data['patches_gold']) == 4:
                    labels.extend(center_of_patch_equal_one(data))
                    number_done += data['patches_gold'].shape[0]
                    pbar.update(number_done)
            pbar.finish()

            classes_in_image, counts = np.unique(labels, return_counts=True)
            for j, cl in enumerate(classes_in_image):
                if str(cl) not in classes_testing:
                    classes_testing[str(cl)] = [counts[j], 0.0]
                else:
                    classes_testing[str(cl)][0] += counts[j]

            results_testing[str(i)] = [[patches_coordinates[j, :].tolist(), labels[j]] for j in range(len(labels))]

        global_results_patches['testing'] = results_testing

        count_max_class, max_class = 0, ''
        for cl in classes_testing:
            if classes_testing[cl][0] > count_max_class:
                max_class = cl
        for cl in classes_testing:
            classes_testing[cl][1] = classes_testing[cl][0] / float(classes_testing[max_class][0])

        global_results_patches['statistics'] = {'classes_training': classes_training, 'classes_testing': classes_testing}

        with open(path_output + 'patches.json', 'w') as outfile:
            json.dump(global_results_patches, outfile)

class Trainer():
    def __init__(self, datasets_dict_path, patches_dict_path, classifier_model, fct_feature_extraction, param_training, results_path, model_path):

        with open(datasets_dict_path) as outfile:    
            datasets_dict = json.load(outfile)

        with open(patches_dict_path) as outfile:    
            patches_dict = json.load(outfile)

        self.dataset_path = sct.slash_at_the_end(str(datasets_dict['dataset_path']), slash=1)

        self.dataset_stats = patches_dict['statistics']
        self.patch_info = patches_dict['patch_info']

        self.training_dataset = datasets_dict['training']
        self.fname_training_raw_images = datasets_dict['training']['raw_images']
        self.fname_training_gold_images = datasets_dict['training']['gold_images']
        self.coord_label_training_patches = patches_dict['training']

        self.testing_dataset = datasets_dict['testing']
        self.fname_testing_raw_images = datasets_dict['testing']['raw_images']
        self.fname_testing_gold_images = datasets_dict['testing']['gold_images']
        self.coord_testing_patches = patches_dict['testing']

        self.model_name = classifier_model['model_name']
        self.model = classifier_model['model']

        self.model_hyperparam = classifier_model['model_hyperparam']

        self.fct_feature_extraction = fct_feature_extraction

        self.param_training = param_training
        if 'nb_iter_hyperparam_search' in self.param_training:
            self.nb_iter_hyperparam_search = self.param_training['nb_iter_hyperparam_search']
        else:
            self.nb_iter_hyperparam_search = 20

        self.results_path = sct.slash_at_the_end(results_path, slash=1)
        self.model_path = sct.slash_at_the_end(model_path, slash=1)
        self.train_model_path = self.model_path + self.model_name + '_init.pkl'

        with open(self.train_model_path, 'w') as outfile:
            pickle.dump(self.model, outfile)

    def prepare_patches(self, ratio_patch_per_image=1.0):

        coord_prepared = {}
        label_prepared = {}

        for i, fname in enumerate(self.fname_training_raw_images):
            nb_patches_tot = len(self.coord_label_training_patches[str(i)])
            nb_patches_to_extract = int(ratio_patch_per_image * nb_patches_tot)

            coord_prepared[str(i)] = []
            label_prepared[str(i)] = []
            for i_patch in range(nb_patches_to_extract):
                coord_prepared[str(i)].append(self.coord_label_training_patches[str(i)][i_patch][0])
                label_prepared[str(i)].append(self.coord_label_training_patches[str(i)][i_patch][1])

        return coord_prepared, label_prepared


    def extract_patch_feature_label_from_image(self, path_dataset, fname_raw_images, fname_gold_images, patches_coordinates, patches_labels):

        patch_size = self.patch_info['patch_size']  # [int, int]
        patch_pixdim = self.patch_info['patch_pixdim']  # {'axial': [float, float], 'sagittal': [float, float], 'frontal': [float, float]}

        raw_images = [Image(path_dataset + fname) for fname in fname_raw_images]

        for k in range(len(patches_coordinates)):

            ind = [patches_coordinates[k][0], patches_coordinates[k][1], patches_coordinates[k][2]]
            label = int(patches_labels[k])

            patches_raw, patches_feature = [], []

            if 'axial' in patch_pixdim:
                range_x = np.linspace(ind[0] - (patch_size[0] / 2.0) * patch_pixdim['axial'][0], ind[0] + (patch_size[0] / 2.0) * patch_pixdim['axial'][0], patch_size[0])
                range_y = np.linspace(ind[1] - (patch_size[1] / 2.0) * patch_pixdim['axial'][1], ind[1] + (patch_size[1] / 2.0) * patch_pixdim['axial'][1], patch_size[1])
                coord_x, coord_y = np.meshgrid(range_x, range_y)
                coord_x = coord_x.ravel()
                coord_y = coord_y.ravel()
                coord_physical = [[coord_x[i], coord_y[i], ind[2]] for i in range(len(coord_x))]

                for raw_image in raw_images:
                    grid_voxel = np.array(raw_image.transfo_phys2continuouspix(coord_physical))
                    patch = np.reshape(raw_image.get_values(np.array([grid_voxel[:, 0], grid_voxel[:, 1], grid_voxel[:, 2]]),
                                                            interpolation_mode=1), (patch_size[0], patch_size[1]))
                    patches_raw.append(np.expand_dims(patch, axis=0))
                    patches_feature.append(self.fct_feature_extraction(patch))

            if 'sagittal' in patch_pixdim:
                range_x = np.linspace(ind[0] - (patch_size[0] / 2.0) * patch_pixdim['sagittal'][0], ind[0] + (patch_size[0] / 2.0) * patch_pixdim['sagittal'][0], patch_size[0])
                range_y = np.linspace(ind[1] - (patch_size[1] / 2.0) * patch_pixdim['sagittal'][1], ind[1] + (patch_size[1] / 2.0) * patch_pixdim['sagittal'][1], patch_size[1])
                coord_x, coord_y = np.meshgrid(range_x, range_y)
                coord_x = coord_x.ravel()
                coord_y = coord_y.ravel()
                coord_physical = [[ind[0], coord_x[i], coord_y[i]] for i in range(len(coord_x))]

                for raw_image in raw_images:
                    grid_voxel = np.array(raw_image.transfo_phys2continuouspix(coord_physical))
                    patch = np.reshape(raw_image.get_values(np.array([grid_voxel[:, 0], grid_voxel[:, 1], grid_voxel[:, 2]]),
                                                            interpolation_mode=1), (patch_size[0], patch_size[1]))
                    patches_raw.append(np.expand_dims(patch, axis=0))
                    patches_feature.append(self.fct_feature_extraction(patch))

            if 'frontal' in patch_pixdim:
                range_x = np.linspace(ind[0] - (patch_size[0] / 2.0) * patch_pixdim['frontal'][0], ind[0] + (patch_size[0] / 2.0) * patch_pixdim['frontal'][0], patch_size[0])
                range_y = np.linspace(ind[1] - (patch_size[1] / 2.0) * patch_pixdim['frontal'][1], ind[1] + (patch_size[1] / 2.0) * patch_pixdim['frontal'][1], patch_size[1])
                coord_x, coord_y = np.meshgrid(range_x, range_y)
                coord_x = coord_x.ravel()
                coord_y = coord_y.ravel()
                coord_physical = [[coord_x[i], ind[1], coord_y[i]] for i in range(len(coord_x))]

                for raw_image in raw_images:
                    grid_voxel = np.array(raw_image.transfo_phys2continuouspix(coord_physical))
                    patch = np.reshape(raw_image.get_values(np.array([grid_voxel[:, 0], grid_voxel[:, 1], grid_voxel[:, 2]]),
                                                            interpolation_mode=1), (patch_size[0], patch_size[1]))
                    patches_raw.append(np.expand_dims(patch, axis=0))
                    patches_feature.append(self.fct_feature_extraction(patch))

            patches_raw = np.concatenate(patches_raw, axis=0)
            patches_feature = np.concatenate(patches_feature, axis=0)

            yield {'patches_raw': patches_raw, 'patches_feature': patches_feature, 'patches_label': label}


    def get_minibatch_patch_feature_label(self, patch_iter, size):
        """Extract a minibatch of examples, return a tuple X_text, y.

        Note: size is before excluding invalid docs with no topics assigned.

        """
        data = [(patch['patches_raw'], patch['patches_feature'], patch['patches_label']) for patch in itertools.islice(patch_iter, size)]

        if not len(data):
            return {'patches_raw': np.asarray([], dtype=np.float), 'patches_feature': np.asarray([], dtype=np.float), 'patches_label': np.asarray([], dtype=int)}

        patches_raw, patches_feature, patches_label = zip(*data)
        patches_raw, patches_feature, patches_label = np.asarray(patches_raw, dtype=np.float), np.asarray(patches_feature, dtype=np.float), np.asarray(patches_label, dtype=int)

        return {'patches_raw': patches_raw, 'patches_feature': patches_feature, 'patches_label': patches_label}

    def iter_minibatches2(self, coord_dict_train_prepared, label_dict_prepared, minibatch_size):

        # temp_minibatch = {'patches_raw': np.empty( shape=(0, 0, 0, 0) ), 'patches_gold': np.empty( shape=(0, 0, 0, 0) )} # len=0 
        temp_minibatch = {'patches_raw': np.empty( shape=(0, 0, 0, 0) ), 'patches_feature': np.empty( shape=(0, 0) ), 'patches_label': np.empty( shape=(0,) )} # len=0 

        for index_fname_image in coord_dict_train_prepared:

            fname_raw_cur = map(str, self.fname_training_raw_images[int(index_fname_image)])
            fname_gold_cur = map(str, self.fname_training_gold_images[int(index_fname_image)])
            
            stream_data = self.extract_patch_feature_label_from_image(path_dataset=self.dataset_path,
                                                         fname_raw_images=fname_raw_cur,
                                                         fname_gold_images=fname_gold_cur,
                                                         patches_coordinates=coord_dict_train_prepared[str(index_fname_image)],
                                                         patches_labels=label_dict_prepared[str(index_fname_image)])

            # stream_data = extract_patches_from_image(path_dataset=self.dataset_path,
            #                                              fname_raw_images=fname_raw_cur,
            #                                              fname_gold_images=fname_gold_cur,
            #                                              patches_coordinates=coord_dict_train_prepared[str(index_fname_image)],
            #                                              patch_info=self.patch_info,
            #                                              verbose=1)

            minibatch = self.get_minibatch_patch_feature_label(stream_data, minibatch_size - temp_minibatch['patches_raw'].shape[0])
            # # minibatch = get_minibatch(stream_data, minibatch_size - temp_minibatch['patches_raw'].shape[0])


            # if minibatch['patches_raw'].shape[0] == minibatch_size:
            #     yield minibatch
            # else:
            #     if temp_minibatch['patches_raw'].shape[0] == 0:
            #         temp_minibatch = minibatch # len!=0
            #     else:
            #         patches_raw_temp = np.concatenate([temp_minibatch['patches_raw'], minibatch['patches_raw']], axis=0)
            #         patches_gold_temp = np.concatenate([temp_minibatch['patches_feature'], minibatch['patches_feature']], axis=0)
            #         patches_gold_temp = np.concatenate([temp_minibatch['patches_label'], minibatch['patches_label']], axis=0)
            #         minibatch = {'patches_raw': patches_raw_temp, 'patches_feature': patches_feature, 'patches_label': patches_gold_temp} # concat
            #         if minibatch['patches_raw'].shape[0] == minibatch_size:
            #             # temp_minibatch = {'patches_raw': np.empty( shape=(0, 0, 0, 0) ), 'patches_gold': np.empty( shape=(0, 0, 0, 0) )}
            #             temp_minibatch = {'patches_raw': np.empty( shape=(0, 0, 0, 0) ), 'patches_feature': np.empty( shape=(0, 0) ), 'patches_label': np.empty( shape=(0,) )}
            #             yield minibatch
            #         else:
            #             temp_minibatch = minibatch

#########################################
# USE CASE
#########################################
def extract_list_file_from_path(path_data):
    ignore_list = ['.DS_Store']
    sct.printv('Extracting ' + path_data)
    cr = '\r'

    list_data = []
    for root, dirs, files in os.walk(path_data):
        for fname_im in files:
            if fname_im in ignore_list:
                continue
            if 'seg' in fname_im or 'gmseg' in fname_im:
                continue
            f_seg = None
            for fname_seg in files:
                if fname_im[:-7] in fname_seg:
                    f_seg = fname_seg
            list_data.append([[fname_im], [f_seg]])

    return list_data


def extract_hog_feature(im, param=None):

    if param is None:
        param = {'orientations': 8, 'pixels_per_cell': [6, 6], 'cells_per_block': [3,3],
                'visualize': False, 'transform_sqrt': True}

    hog_feature = np.array(hog(image = im, orientations=param['orientations'],
                pixels_per_cell=param['pixels_per_cell'], cells_per_block=param['cells_per_block'],
                transform_sqrt=param['transform_sqrt'], visualise=param['visualize']))

    return hog_feature

def extract_patch_feature(im, param=None):

    return im

def normalization_percentile(sct_img, param, model=None):

    if param is None:
        param = {'range': [0,255]}

    sct_img.data = param['range'][0] + param['range'][1] * (sct_img.data - np.percentile(sct_img.data, 0)) / np.abs(np.percentile(sct_img.data, 0) - np.percentile(sct_img.data, 100))

    return sct_img


def center_of_patch_equal_one(data):
    patch_size_x, patch_size_y = data['patches_gold'].shape[2], data['patches_gold'].shape[3]
    return np.squeeze(data['patches_gold'][:, 0, int(patch_size_x / 2), int(patch_size_y / 2)])


my_file_manager = FileManager(dataset_path='/Volumes/folder_shared-1/benjamin/machine_learning/patch_based/large_nobrain_nopad/',
                              fct_explore_dataset=extract_list_file_from_path,
                              patch_extraction_parameters={'ratio_dataset': [0.04, 0.02],
                                                           'ratio_patches_voxels': 0.001,
                                                           'patch_size': [32, 32],
                                                           'patch_pixdim': {'axial': [1.0, 1.0]},
                                                           'extract_all_positive': False,
                                                           'extract_all_negative': False,
                                                           'batch_size': 100},
                              fct_groundtruth_patch=None)

path_output = '/Users/chgroc/data/spine_detection/model/'

# training_dataset, testing_dataset = my_file_manager.decompose_dataset(path_output)
# my_file_manager.explore()

from sklearn.svm import SVC
svm_model = {'model_name': 'SVM', 'model': SVC(), 'model_hyperparam':{'C': [1, 10, 100, 1000], 'kernel': ['linear']}}

methode_normalization_1={'methode_normalization_name':'histogram', 'param':{'cutoffp': (1, 99), 
                            'landmarkp': [10, 20, 30, 40, 50, 60, 70, 80, 90], 'range': [0,255]}}
methode_normalization_2={'methode_normalization_name':'percentile', 'param':{'range': [0,255]}}

param_training = {'batch_size': 500, 'number_of_epochs': 1, 'nb_iter_hyperparam_search': 20, 'patch_size': [32, 32]}

results_path = '/Users/chgroc/data/spine_detection/results/'
model_path = '/Users/chgroc/data/spine_detection/model/'

my_trainer = Trainer(datasets_dict_path = path_output + 'datasets.json', patches_dict_path= path_output + 'patches.json', 
                        classifier_model=svm_model,
                        fct_feature_extraction=extract_patch_feature, 
                        param_training=param_training, 
                        results_path=results_path, model_path=model_path)

coord_prepared, label_prepared = my_trainer.prepare_patches(0.5)
minibatch_iterator_test = my_trainer.iter_minibatches2(coord_prepared, label_prepared, 1000)
