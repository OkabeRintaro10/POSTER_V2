from main import *
from deepface import DeepFace

# Checking for all types of devices available
if torch.backends.mps.is_available():
    device = "mps"
elif torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

print(f"Using device: {device}")
# Predicting the model
# def prediction(model, image_path):
model = pyramid_trans_expr2(img_size=224, num_classes=7)

model = torch.nn.DataParallel(model)
model = model.to(device)

model_path = "raf-db-model_best.pth"
image_path = "/Users/futuregadgetlab/Developer/GitRepos/POSTER_V2/raf-db/DATASET/test/5/test_0119_aligned.jpg"


def predict(model, image_path):
    with torch.no_grad():
        transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
                transforms.RandomErasing(p=1, scale=(0.05, 0.05)),
            ]
        )
        img1 = DeepFace.detectFace(test_image)
        plt.imshow(img1)
        test_image = Image.open(image_path)
        image_tensor = transform(test_image).unsqueeze(0)
        image_tensor = image_tensor.to(device)

        model.eval()
        img_pred = model(image_tensor)
        topk = (3,)
        with torch.no_grad():
            maxk = max(topk)
            # batch_size = target.size(0)
            _, pred = img_pred.topk(maxk, 1, True, True)
            pred = pred.t()

        img_pred = pred
        img_pred = img_pred.squeeze().cpu().numpy()
        im_pre_label = np.array(img_pred)
        y_pred = im_pre_label.flatten()
        print(f"The predicted labels are {y_pred}")
