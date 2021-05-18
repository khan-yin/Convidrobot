var likeTimes = [];
var heart = document.querySelectorAll('.like');
var likeNum = document.querySelectorAll('.like-num');

//请求用户所发表文章的数据
$.ajax({
    url: "http://47.103.193.240:8000/robot/getcomments/",
    type: "GET",
    success: function(msg) {
        for (let i=0;i<heart.length;i++){
            likeNum[i].innerText = msg[i].star;
        }
    },
    error: function() {
        alert('网络错误')//失败
    }
});

// 点赞动画
for (let i =0;i<heart.length;i++){
    likeTimes.push(0);
    heart[i].onclick = function () {
        if (likeTimes[i]%2===0){
            heart[i].style.animation='like  .8s steps(28) 1';
            heart[i].style.backgroundPosition='right';
            heart[i].style.color='#ee5253';
            likeNum[i].innerText = parseInt(likeNum[i].innerText)+1;
            $.ajax({
                url: "http://47.103.193.240:8000/robot/addstar/",
                type: "POST",
                data: {'id':i+1},
                success: function(msg) {
                    console.log(i+1);
                    console.log(msg);
                },
                error: function() {
                    alert('网络错误')//失败
                }
            });
        }
        else {
            heart[i].style.animation='unlike  .8s steps(28) 1';
            heart[i].style.backgroundPosition='left';
            heart[i].style.color='#576574';
            likeNum[i].innerText = parseInt(likeNum[i].innerText)-1;
            $.ajax({
                url: "http://47.103.193.240:8000/robot/deletestar/",
                type: "POST",
                data: {'id':i+1},
                success: function(msg) {
                    console.log(i+1);
                    console.log(msg);
                },
                error: function() {
                    alert('网络错误')//失败
                }
            });
        }
        likeTimes[i]++;
    }
}