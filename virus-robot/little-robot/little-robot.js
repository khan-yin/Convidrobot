//小飞机器人组件
Vue.component('little-robot',{
	mode:'hash',
	template:'<div><div class="menu-box">\n' +
		'    <div class="menu-logo">\n' +
		'        <a href="javascript:void(0);" @click="postOpenPlatform(\'../message/message.html\')"><img src="../image/comment.png" style="height: 20px;width:20px;position: relative;left: 1px;top: 3px"></a>\n' +
		'        <div class="menu-border">\n' +
		'        </div>\n' +
		'    </div>\n' +
		'    <div class="menu-logo">\n' +
		'        <a href="../visual-data/visual-data.html"><img src="../image/data.png" style="height: 25px;width:25px;position: relative;left: 1px;top: 3px"></a>\n' +
		'        <div class="menu-border">\n' +
		'        </div>\n' +
		'    </div>\n' +
		'    <div class="menu-logo">\n' +
		'        <a href="../doctor/doctor.html"><img src="../image/AI.png" style="height: 25px;width:25px;position: relative;left: 1px;top: 3px"></a>\n' +
		'        <div class="menu-border">\n' +
		'        </div>\n' +
		'    </div>\n' +
		'    <div class="menu-logo">\n' +
		'        <a href="../news/news.html"><img src="../image/news.png" style="height: 25px;width:25px;position: relative;left: 1px;top: 3px"></a>\n' +
		'        <div class="menu-border">\n' +
		'        </div>\n' +
		'    </div>\n' +
		'</div>\n' +
		'<div class="little-robot">\n' +
		'    <div class="little-robot-eye"></div>\n' +
		'    <div class="little-robot-eye"></div>\n' +
		'    <div class="little-robot-mouth"></div>\n' +
		'</div>\n' +
		'<div class="little-answer">\n' +
		'   <div style="width: 160px;position: absolute;left: 20px;top: 10px">\n' +
		'       <a id=\'little-text\'>点击我打开导航栏哦~</a>\n' +
		'   </div>\n' +
		'</div></div>'
});
var vm = new Vue({
	el:"#side-menu",
	data:{

	}
});
var clicktimes = 0;
var littleRobot = document.querySelector('.little-robot');
var logo = document.querySelectorAll('.menu-logo');
littleRobot.onclick=function(e){
	e?e.stopPropagation():event.cancelBubble = true;
	var logo = document.querySelectorAll('.menu-logo');
	if (clicktimes%2===0){
		for (let i = 0 ;i<logo.length;i++){
			let s = (30+70*i)+'px';
			logo[i].style.bottom=s;
		}
	}
	else {
		for (let i = 0 ;i<logo.length;i++){
			logo[i].style.bottom='-58px';
		}
	}
	clicktimes++;
};
var URL = ['../message/message.html','../visual-data/visual-data.html','../doctor/doctor.html','../news/news.html'];
for (let i =0;i<logo.length;i++){
	logo[i].onclick = function (e) {
		e?e.stopPropagation():event.cancelBubble = true;
		window.location.href=URL[i];
	}
}
$(document).click(function () {
	for (let i = 0 ;i<logo.length;i++){
		logo[i].style.bottom='-58px';
	}
	if (clicktimes%2===1)clicktimes++;
});
//实现机器人提示小贴士
var flag=0;
var tipsWord=['点击我打开导航栏哦~',
	'小飞是会图像分析、AI聊天的智能机器人哦~我还在继续努力学习~',
	'如必须乘坐公共交通工具，务必全程佩戴口罩，途中尽量避免用手触摸车上物品。',
	'小飞，要努力变得更聪明~',
	'办公时保持办公区环境清洁，每日通风3次以上，每次20-30分钟.',
	'在食堂要采取分散错时用餐，尽可能减少人员聚集,往返食堂请全程佩戴口罩',
	'建议适当、适度进行运动，增强身体免疫能力，保持身体状态良好。避免过量运动。',
	'防疫期间，摘口罩前后做好双手清洁卫生；请自觉将废弃口罩放入专用垃圾桶内。',
	'新冠病毒主要传播方式是经呼吸道飞沫传播，也可通过接触传播。'];
setInterval(function () {
	if (flag%2===0) {
		let i =(tipsWord.length*Math.random()).toFixed(0);
		$('#little-text').text(tipsWord[i]);
		$('.little-answer').show(600);
	}
	else $('.little-answer').hide(600);
	flag++;
},5000);
