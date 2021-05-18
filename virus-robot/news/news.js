/**
 * @function 获取新闻
 * @description 通过ajax访问对应的api接口，获取新闻数据，并将新闻数据渲染到界面中
 * @return void
 * @author Wu 2020/04/16
 */
function getNews() {
    $.ajax({
        type: "get",
        url: "http://49.232.173.220:3001/data/getTimelineService",
        dataType: "json",
        async: false,
        success: function (data) {
            let newsBox = document.querySelectorAll('.news-box');
            let title = document.querySelectorAll('.title');
            let summary = document.querySelectorAll('.summary');
            let date = document.querySelectorAll('.date');
            for (let i = 0;i<newsBox.length;i++){
                let ran =(10*Math.random()).toFixed(0);
                let index =((i*10+ran)*Math.random()).toFixed(0);
                title[i].innerText=data[index].title;
                let s1 = data[index].sourceUrl;
                title[i].setAttribute('href',s1);
                let s =data[index].summary;
                if (s.length>=50){
                    summary[i].innerText = s.substring(0,50)+'...';
                }
                else summary[i].innerText = s;
                date[i].innerText = data[index].pubDateStr+' '+data[index].infoSource;
            }
        }
    });
}
getNews();