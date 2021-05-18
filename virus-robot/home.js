/**
 * @function 实现搜索功能
 * @description 处理用户输入的信息，进行谣言查询、各地数据查询、进入小飞问答界面等功能
 * @return void
 * @author Wu 2020/04/16
 */
function search(){
    question = document.querySelector('.question');
    s=question.value;
    console.log(s);
    //求证谣言
    if(s[0]==='求'&&s[1]==='证'&&s[2]===' '){
        $.ajax({
            type: "get",
            url: "http://49.232.173.220:3001/data/getIndexRumorList",
            dataType: "json",
            async: false,
            success: function(data){
                let flag = false;
                //console.log(data);
                //$('.home-news').css('display','block');
                let patt= s.replace(/求证 /i,"");
                patt = new RegExp(patt);
                for (let i = 0;i<data.length;i++){
                    if (patt.test(data[i].title) === true){
                        $('#data').slideUp(0);
                        $('#rumor').slideDown(600);
                        $('#rumor-title').text(data[i].title);
                        $('#rumor-summary').text('结论： '+data[i].mainSummary);
                        $('#rumor-body').text(data[i].body);
                        flag=true;
                    }
                }
                if (flag===false){
                    $('#rumor').slideUp(0);
                    $('#data').slideDown(600);
                    $("#data-title").text('我好像不明白~');
                    $('#data-content').text('可以输入“更多”进入聊天室，\n也许我可以为您提供更多帮助哦~');
                }
            }
        });
    }
    //查询各地数据
    else if (s[0]==='查'&&s[1]==='询'&&s[2]===' '){
        $('#rumor').slideUp(0);
        //查询国外数据
        if(s[4]==='内'){
            $.ajax({
                type: "get",
                url: "http://47.103.193.240:8000/robot/datamap/",
                dataType: "json",
                async: false,
                success: function (data) {
                    data =data.data;
                    let province=-1,city=-1;
                    let str= s.replace(/查询 国内 /i,"");
                    for(let i=0;i<data.length;i++){
                        if(str.search(data[i].name)!==-1){
                            province=i;
                        }
                        for (let j=0;j<data[i].children.length;j++){
                            if(str.search(data[i].children[j].name)!==-1){
                                city=j;
                                break;
                            }
                        }
                    }
                    //查询市级行政区
                    if (city>=0){
                        let total = data[province].children[city].total;
                        $('#data').slideDown(600);
                        $("#data-title").text(str+'的数据为：');
                        $("#data-content").text("总共确诊:"+total.confirm+"\n"+
                            "死亡："+total.dead+"\n" +
                            "死亡率："+total.deadRate+"%\n" +
                            "治愈："+total.heal+"\n" +
                            "治愈率："+total.healRate+"%\n" +
                            "现存确诊："+total.nowConfirm+"\n" +
                            "疑似："+total.suspect);
                    }
                    //查询省级行政区
                    else if(province>=0&&city===-1){
                        let total = data[province].total;
                        $('#data').slideDown(600);
                        $("#data-title").text(str+'的数据为：');
                        $("#data-content").text("总共确诊:"+total.confirm+"\n"+
                            "死亡："+total.dead+"\n" +
                            "死亡率："+total.deadRate+"%\n" +
                            "治愈："+total.heal+"\n" +
                            "治愈率："+total.healRate+"%\n" +
                            "现存确诊："+total.nowConfirm+"\n" +
                            "疑似："+total.suspect);
                    }
                }
            });
        }
        //查询国际数据
        else if(s[4]==='际'){
            let important = false;
            let str= s.replace(/查询 国际 /i,"");
            $.ajax({
                type: "get",//请求方式
                url: "http://49.232.173.220:3001/data/getStatisticsService",//地址，就是json文件的请求路径
                dataType: "json",//数据类型可以为 text xml json  script  jsonp
                async: false,
                success: function (data) {
                    country = data.importantForeignTrendChart;
                    for (let i=0;i<country.length;i++){
                        if (country[i].title.search(str)!==-1){
                            important=true;
                            $('#data-img').attr('src',country[i].imgUrl);
                            $('#data-img').show();
                        }
                        else if (str=='中国'){
                            important=true;
                            $('#data-img').attr('src','https://img1.dxycdn.com/2020/0324/278/3403801351376518263-135.png');
                            $('#data-img').show();
                        }
                    }
                }
            });
            $.ajax({
                type: "get",//请求方式
                url: "http://49.232.173.220:3001/data/getListByCountryTypeService2true",//地址，就是json文件的请求路径
                dataType: "json",//数据类型可以为 text xml json  script  jsonp
                async: false,
                success: function (data){
                    if (important===false) $('#data-img').hide();
                    for (let i=0;i<data.length;i++){
                        if (data[i].provinceName===str||data[i].countryFullName===str||data[i].countryShortCode===str){
                            total=data[i];
                            $('#data').slideDown(600);
                            $("#data-title").text(str+'的数据为：');
                            $("#data-content").text("总共确诊:"+total.confirmedCount+"\n"+
                                "死亡："+total.deadCount+"\n" +
                                "死亡率："+total.deadRate+"%\n" +
                                "治愈："+total.curedCount+"\n" +
                                "治愈率："+(total.curedCount/total.confirmedCount*100).toFixed(2)+"%\n" +
                                "现存确诊："+total.currentConfirmedCount+"\n" +
                                "疑似："+total.suspectedCount);

                        }
                    }
                }
            });
        }
    }
    else if(s==='更多'){
        $('#rumor').slideUp(0);
        window.location.href='chat/chat.html';
    }
    //输入不符合格式或查询失败
    else {
        $('#rumor').slideUp(0);
        $('#data').slideDown(600);
        $("#data-title").text('我好像不明白~');
        $('#data-content').text('可以输入“更多”进入聊天室，\n也许我可以为您提供更多帮助哦~');
    }
}

//对话框动画
question = document.querySelector('.question');
question.onfocus=function () {
    $('.question-form').css('width','40%');
    $('.question-form').css('left','30%');
    console.log(question.value);
    document.onkeydown=function (event) {
        if (event.keyCode===13)search()
    }
};
question.onblur=function () {
    $('.question-form').css('width','15%');
    $('.question-form').css('left','42.5%');
    $('#rumor').slideUp(600);
    $('#data').slideUp(600);
    question.value='';
};