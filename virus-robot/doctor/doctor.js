/**
 * @function 上传图片
 * @description 将图片上传至后端，并做出反应
 * @return void
 * @author Wu 2020/04/16
 */
function upload(){
    var fileObj = document.getElementById('img-file').files; //创建一个forData
    var reader = new FileReader();
    reader.onload = function(evt){
        var imgstr = evt.target.result; //这就是base64字符串
        $.ajax({
            url: "http://47.103.193.240:8000/robot/getphoto/",
            type: "POST",
            data:{
                "data": imgstr
            },
            success: function(data) {
                data=JSON.parse(data);
                console.log(data);
                $('#result-score').text('患肺炎的概率为'+(data.pred*100).toFixed(2)+'%');
                if (data.pred>=0.7){
                    $('#face').attr('src','../image/bad.png');
                }
                else if (data.pred>=0.4){
                    $('#face').attr('src','../image/normal.png');
                }
                else{
                    $('#face').attr('src','../image/good.png');
                }
                $('#color-photo').attr('src','');
                $('#pre-photo').css("display","none");
                $('#color-photo').css("display","block");
                $('.change-img').css("display","block");
                $('#color-photo').attr('src',data.newphotourl+'?'+new Date().getTime());
            },
            error: function() {
                console.log('error');
            }
        })
    };
    //正式读取文件
    reader.readAsDataURL(fileObj[0]);

}

/**
 * @function 预览图片
 * @description 在文件框中选中图片，并将选中的图片显示在页面中
 * @return boolean
 * @author Wu 2020/04/16
 */
function setImagePreview() {
    var docObj=document.querySelector('#img-file');

    var imgObjPreview=document.querySelector('.photo');
    if(docObj.files && docObj.files[0]){
        //火狐下，直接设img属性
        imgObjPreview.style.display = 'block';
        imgObjPreview.style.height = '100%';
        imgObjPreview.style.width = '100%';
        imgObjPreview.style.left='0';
        imgObjPreview.style.top='0';
        //imgObjPreview.src = docObj.files[0].getAsDataURL();

        $('#pre-photo').css("display","block");
        $('#color-photo').css("display","none");
        $('.change-img').css("display","none");
        //火狐7以上版本不能用上面的getAsDataURL()方式获取，需要一下方式
        imgObjPreview.src = window.webkitURL.createObjectURL(docObj.files[0]);
    }else{
        //IE下，使用滤镜
        docObj.select();
        var imgSrc = document.selection.createRange().text;
        var localImagId = document.getElementById("localImag");
        imgObjPreview.style.display = 'block';
        localImagId.style.width = "100%";
        localImagId.style.height = "100%";
        imgObjPreview.style.left='0';
        imgObjPreview.style.top='0';
        $('#pre-photo').css("display","block");
        $('#color-photo').css("display","none");
        $('.change-img').css("display","none");
        //图片异常的捕捉，防止用户修改后缀来伪造图片
        try{
            localImagId.style.filter="progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod=scale)";
            localImagId.filters.item("DXImageTransform.Microsoft.AlphaImageLoader").src = imgSrc;
        }catch(e){
            alert("您上传的图片格式不正确，请重新选择!");
            return false;
        }
        imgObjPreview.style.display = 'block';
        document.selection.empty();
    }
    return true;
}

/**
 * @function 切换图片
 * @description 点击切换按钮，可以切换X光图片是否有标注
 * @return
 * @author Wu 2020/05/28
 */
function changeImage() {
    if ($('#pre-photo').css("display") === "block"){
        $('#pre-photo').css("display","none");
        $('#color-photo').css("display","block");
    }
    else {
        $('#pre-photo').css("display","block");
        $('#color-photo').css("display","none");
    }
}

$('.change-img').click(function () {
    changeImage();
});