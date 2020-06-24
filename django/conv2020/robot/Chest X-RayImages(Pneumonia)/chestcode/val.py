
from .util import *


def test_model(model):
    running_correct = 0.0
    running_total = 0.0
    true_labels = []
    pred_labels = []
    dataloaders, dataset_sizes, class_names = load_data()
    with torch.no_grad():
        for data in dataloaders[TEST]:
            inputs, labels = data
            inputs = inputs.to(device)
            labels = labels.to(device)
            true_labels.append(labels.item())
            outputs = model(inputs)
            _, preds = torch.max(outputs.data, 1)
            pred_labels.append(preds.item())
            running_total += labels.size(0)
            running_correct += (preds == labels).sum().item()
        acc = running_correct/running_total
    return true_labels, pred_labels, running_correct, running_total, acc


def evaluate_model(modelID=-1):
    model_list = os.listdir(model_dir)
    print(model_list)
    if modelID >= len(model_list):
        print("can't find pretrained model {}".format(modelID))
    model = torch.load(model_dir+model_list[modelID])
    true_labels, pred_labels, running_correct, running_total, acc = test_model(model)
    print("Total Correct: {}, Total Test Images: {}".format(running_correct, running_total))
    print("Test Accuracy: ", acc)

    cm = confusion_matrix(true_labels, pred_labels)
    # a nice hack for binary classification
    tn, fp, fn, tp = cm.ravel()
    recall = tp/(tp + fn)
    precision = tp/(tp + fp)
    f1_score = 2 * (recall * precision)/(precision + recall)
    print("F1 Score:", f1_score)

    ax = sns.heatmap(cm, annot=True, fmt="d")
    plt.show()


def predict_single_img(img_file, modelID=-1,model_name="best.pth"):
    model_list = os.listdir(model_dir)
    img = io.imread(img_file, as_gray=True)
    img = np.expand_dims(img, axis=2)
    img = np.concatenate((img, img, img), axis=-1)
    #print(img.shape)
    if img.dtype is not np.uint8:
        img *= 255
        img = img.astype(np.uint8)
    img = Image.fromarray(img)
    transform = data_transforms(TEST)

    model_file = os.path.join(model_dir, os.listdir(model_dir)[-1], model_name)
    model = torch.load(model_dir+model_list[modelID]).to(device)
    input = transform(img).unsqueeze(0).to(device)
    print(input.shape)
    out = model(input)
    out = torch.softmax(out, -1)
    print(out)
    prob = out.detach().cpu().numpy()[0]
    print("Likelihood of NORMAL is {} and PNEUMONIA is {}.".format(prob[0], prob[1]))

if __name__ == '__main__':
    #evaluate_model()
    predict_single_img("./img/test.jpeg")
