#!/usr/bin/env python
# coding: utf-8


from .util import *

def plot_loss_acc(epochLossRecord, epochAccRecord, savedir=None, title="loss_accuracy"):
    if savedir is None:
        savedir = os.path.join(model_dir, os.listdir(model_dir)[-1])

    epochNum = len(epochLossRecord[TRAIN])

    fig, axs = plt.subplots(2, 1, figsize=(18, 10))
    axs[0].set_xlabel('epoch')
    axs[0].set_ylabel('loss')
    axs[0].plot(range(epochNum), epochLossRecord[TRAIN],
                label="train", color='tab:orange')
    axs[0].plot(range(epochNum), epochLossRecord[VAL],
                label="valid", color='tab:red')
    axs[0].legend()
    axs[0].grid(True)

    axs[1].set_xlabel('epoch')
    axs[1].set_ylabel('accuracy')
    axs[1].plot(range(epochNum), epochAccRecord[TRAIN],
                label="train", color='tab:blue')
    axs[1].plot(range(epochNum), epochAccRecord[VAL],
                label="valid", color='tab:green')
    axs[1].legend()
    axs[1].grid(True)
    plt.savefig(os.path.join(savedir, title + '.pdf'))


def train_model(model, criterion, optimizer, scheduler, num_epochs, dataset_sizes):
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(num_epochs):
        print("Epoch: {}/{}".format(epoch+1, num_epochs))
        print("="*10)

        for phase in [TRAIN, VAL]:
            if phase == TRAIN:
                scheduler.step()
                model.train()
            else:
                model.eval()
            # initialize the parameters
            # compute the loss
            # compute the gradients
            running_loss = 0.0
            running_corrects = 0
            for data in dataloaders[phase]:
                inputs, labels = data
                inputs = inputs.to(device)
                labels = labels.to(device)
                # zero the parameter gradients
                optimizer.zero_grad()
                # forward
                # track history when the phase is train
                with torch.set_grad_enabled(phase==TRAIN):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                phase, epoch_loss, epoch_acc))

            # deep copy the model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())

    print('Best val Acc: {:4f}'.format(best_acc))
    # load best model weights
    model.load_state_dict(best_model_wts)
    return model


def load_pre_model():
    class_names = image_datasets[TRAIN].classes
    model_pre = models.resnet18(pretrained=True)

    for param in model_pre.parameters():
        param.required_grad = False

    num_features = model_pre.fc.in_features
    # Replace last layer
    model_pre.fc = nn.Linear(num_features, len(class_names))

    model_pre = model_pre.to(device)
    return model_pre


def transfer_learning():
    time_now = str(datetime.datetime.now())[:-7]
    model_pre = load_pre_model()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model_pre.parameters(), lr=0.001, momentum=0.9, weight_decay=0.01)
    # Decay LR by a factor of 0.1 every 10 epochs
    exp_lr_scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

    model_pre = train_model(model_pre, criterion, optimizer, exp_lr_scheduler, EPOCHS, dataset_sizes)
    time_now = str(datetime.datetime.now())[:-7].replace(" ", "-").replace(":", "-")
    torch.save(model_pre, model_dir+time_now+".pth")

if __name__ == '__main__':
    transfer_learning()
