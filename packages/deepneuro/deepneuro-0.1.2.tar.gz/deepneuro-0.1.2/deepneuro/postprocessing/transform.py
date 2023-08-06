from deepneuro.postprocessing.postprocessor import Postprocessor
from deepneuro.utilities.util import add_parameter


class Apply_Transform(Postprocessor):

    def load(self, kwargs):

        # Naming parameter
        add_parameter(self, kwargs, 'name', 'Transform')
        add_parameter(self, kwargs, 'postprocessor_string', '_transformed')

        add_parameter(self, kwargs, 'affine')