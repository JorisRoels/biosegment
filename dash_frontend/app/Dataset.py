import logging
import os

import app.api as api
from app.env import ROOT_DATA_FOLDER
from app.image_utils import label_to_colors
from app.utils import get_folder_list
from PIL import Image
from skimage import io as skio

def get_png_image(path):
    assert os.path.exists(path)
    png = Image.open(path)
    return png

class Dataset:
    def __init__(self, dataset_id):
        self.dataset_id = dataset_id
        self.dataset = api.dataset.get(dataset_id)
        self.type = self.dataset["file_type"]
        self.title = self.dataset["title"]
        self.project_id = self.dataset["owner_id"]
        self.segmentations = {}
        self.annotations = {}
        self.models = {}
        self.location = ROOT_DATA_FOLDER / self.dataset['location']
        self.slices = self.get_slices()

    def get_slices(self):
        logging.debug(f"Slices folder: {self.location}")
        assert self.location.is_dir()
        contents = list(self.location.iterdir())
        if self.type == "tiff":
            # presume single TIFF
            path = contents[0]
            return Image.open(str(path))
        elif self.type == "pngseq":
            return [get_png_image(str(p)) for p in contents]
        else:
            logging.error(f"Unkown filetype for dataset: {self.dataset}")
            return None

    def get_models_available(self):
        models = api.model.get_multi_for_project(self.project_id)
        logging.debug(f"Models: {models}")
        self.models = {m["id"]: m for m in models}
        return [{"label": m["title"], "value": m["id"],} for m in models]

    def get_annotations_available(self):
        annotations = api.annotation.get_multi_for_dataset(self.dataset_id)
        logging.debug(f"Annotations: {annotations}")
        self.annotations = {a["id"]: a for a in annotations}
        return [{"label": a["title"], "value": a["id"],} for a in annotations]

    def get_segmentations_available(self):
        segmentations = api.segmentation.get_multi_for_dataset(self.dataset_id)
        logging.debug(f"Segmentations: {segmentations}")
        self.segmentations = {s["id"]: s for s in segmentations}
        return [{"label": m["title"], "value": m["id"],} for m in segmentations]

    def get_slice(self, slice_id):
        if self.type == "tiff":
            self.slices.seek(slice_id)
            return self.slices
        elif self.type == "pngseq":
            return self.slices[slice_id]
        else:
            logging.error(f"Unkown filetype for dataset: {self.dataset}")
            return None

    def get_label(self, segment_id, slice_id):
        try:
            if len(self.segmentations) == 0:
                self.get_segmentations_available()
            labels_folder = ROOT_DATA_FOLDER / self.segmentations[segment_id]['location']
        except:
            logging.debug(
                f"No segment_id key {segment_id} in {self.segmentations.keys()}"
            )
            labels_folder = None
        logging.debug(f"labels_folder: {labels_folder}")
        assert labels_folder.is_dir()
        contents = list(labels_folder.iterdir())
        if self.type == "tiff":
            # presume single TIFF
            path = contents[0]
            logging.debug(f"TiFF path: {path}")
            tiff = skio.MultiImage(str(path))
            image_array = tiff[slice_id]
            recolored_image_array = label_to_colors(
                image_array,
                alpha=[128],
                color_class_offset=1,
                no_map_zero=True,
            )
            png = Image.fromarray(recolored_image_array)
            return png
        elif self.type == "pngseq":
            path = contents[slice_id]
            assert path.exists()
            image_array = skio.imread(str(path))
            recolored_image_array = label_to_colors(
                image_array,
                alpha=[128],
                labels_contiguous=True,
                no_map_zero=True,
            )
            png = Image.fromarray(recolored_image_array)
            return png
        else:
            logging.error(f"Unkown filetype for dataset: {self.dataset}")
            return None

    def get_title(self):
        return self.title

    def get_dimensions(self):
        return {"min": 0, "max": self.dataset["resolution"]["z"]}
