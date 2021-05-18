// 发送信息
function SendMsg()
{
    var text = document.getElementById("text");
    if (text.value == "" || text.value == null)
    {
        alert("发送信息为空，请输入！")
    }
    else
    {
        AddMsg('default', SendMsgDispose(text.value));
        text.value = "";
    }
}
function robotAnswer(text) {
    AddMsg('robot', SendMsgDispose(text));
}
// 发送的信息处理
function SendMsgDispose(detail)
{
    detail = detail.replace("\n", "<br>").replace(" ", "&nbsp;")
    return detail;
}

// 增加信息
function AddMsg(user,content)
{
    var str = CreadMsg(user, content);
    var msgs = document.getElementById("msgs");
    msgs.innerHTML = msgs.innerHTML + str;
}

// 生成内容
function CreadMsg(user, content)
{
    var str = "";
    if(user == 'default')
    {
        str = "<div class=\"msg guest\"><div class=\"msg-right\"><div class=\"msg-host headDefault\"></div><div class=\"msg-ball\">" + content +"</div></div></div>"
    }
    else
    {
        str = "<div class=\"msg robot\"><div class=\"msg-left\" worker=\"小飞\"><div class=\"msg-host photo\" style=\"background-image: url(../image/robot-head.png)\"></div><div class=\"msg-ball\">" + content + "</div></div></div>";
    }
    return str;
}
var sendMesssage = document.querySelector('#submit');
sendMesssage.onclick = function () {
    var text = document.getElementById("text");
    var question = text.value;
    SendMsg();
    console.log(question);
    $.ajax({
        url: "http://47.103.193.240:8000/robot/getanswer/",
        type: "POST",
        data:{
            "data": question
        },
        success: function(data) {
            robotAnswer(data)
        },
        error: function() {
            alert('网络错误')//失败
        }
    });
};