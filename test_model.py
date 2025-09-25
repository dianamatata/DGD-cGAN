#Test model

import os
import glob
from PIL import Image
import torch
from torchvision import transforms
from torchvision.utils import save_image
from nets.networks_Dgd import ResUnet1, ResUnet2, PatchDiscriminator

if torch.cuda.is_available():
    print("CUDA is available. Running on GPU.")
    device = torch.device("gpu")
elif torch.backends.mps.is_available():
    print("CUDA is not available. Running on MPS.")
    device = torch.device("mps")
else:
    print("CUDA and MPS are not available. Running on CPU.")
    device = torch.device("cpu")

G1 = ResUnet1().to(device)
G2 = ResUnet2().to(device)
D = PatchDiscriminator(in_c=3, num_filters=64, n_down=3).to(device)

# Download the model weights https://drive.google.com/file/d/11fJ4WrxLCWIF890PvaHp_EuriKwI6QWl/view?usp=share_link
G1.load_state_dict(torch.load(f'weights/G_dgdgan_epoch_850.pth', map_location=device))
G2.load_state_dict(torch.load(f'weights/G2_dgdgan_epoch_850.pth', map_location=device))
D.load_state_dict(torch.load(f'weights/D_dgdgan_epoch_850.pth', map_location=device))

input_path = '../DATA_Rovailake/galloway_subset'
img_folder = glob.glob(os.path.join(input_path, '*.jpg'))
output_dir = f"../DATA_Rovailake/underwater_image_restoration/DGD-cGAN_galloway"

# Mode eval
G1.eval()
D.eval()

#Data transform
transform = transforms.Compose([transforms.Resize((1024, 1024), transforms.InterpolationMode.BICUBIC)])


## testing 
count = []

for img in img_folder:
    print(img)
    img_test = transform(Image.open(f"{img}"))
    img_test = transforms.ToTensor()(img_test)
    input_img = img_test.unsqueeze_(0)
    input_img = input_img.to(device)
    dewatered_img = G1(input_img)
    dewatered_sample = dewatered_img
    image_name = (img.split('/')[-1][:-4] +'.jpg')
    file_path = os.path.join(output_dir, image_name)
    save_image(dewatered_sample, file_path, normalize=True)

if (len(count) > 1):
    print ("Total imgs: %d" % len(img_folder)) 
