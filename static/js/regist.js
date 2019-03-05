function regist(deal,type){
	var illegal1= /^[a-zA-Z]{1}([a-zA-Z0-9]|[_]){5,19}$//* 用户名格式 */
	var illegal2= /^([a-zA-Z0-9]|[_]){6,20}$/ /* 只能输入6到20个字母数字下划线 */
	var illegal3= /^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$//* 邮箱格式 */
	var illegal4= /^1(3|4|5|7|8)\d{9}$/ /* 手机号格式 */
	if(type == 'uaccount'){
		if(deal.length < 6)
			$('#show_mess1').html('用户名须大于5位')
		else{
			if(!illegal1.exec(deal))
				$('#show_mess1').html('_以外字符,以字母开头')
			else{
				$('#show_mess1').html('')
			}
		}
	}
	if(type == 'upassword'){
		if(!illegal2.exec(deal))
			$('#show_mess2').html('请使用6到20位数字字母下划线')
		else{
			$('#show_mess2').html('')
		}
	}
	if(type == 'enupassword'){
		var pwd = $('#upassword').val();
		if(pwd != deal)
			$('#show_mess3').html('两次密码不一致')
		else{
			$('#show_mess3').html('')
		}
	}
	if(type == 'umail'){
		if(!illegal3.exec(deal))
		{
			$('#show_mess4').html('邮箱格式不正确')
		}
		else
			$('#show_mess4').html('')
	}
	if(type == 'uphone'){
		if(!illegal4.exec(deal))
			$('#show_mess5').html('手机号格式有误')
		else
			$('#show_mess5').html('')
	}
	if(type == 'uqq'){
		if(deal.length > 10 || deal.length < 5)
			$('#show_mess6').html('QQ号格式有误')
		else
			$('#show_mess6').html('')
	}
	if(type == 'uwechat'){
		if(deal.length > 25 || deal.length < 3)
			$('#show_mess7').html('请输入不正确')
		else
			$('#show_mess7').html('')
	}
	
	if(illegal1.exec($('#uaccount').val())  && illegal2.exec($('#upassword').val()) && $('#upassword').val() == $('#enupassword').val())
		{
			$('#next').attr('disabled',false);
			if(illegal3.exec($('#umail').val())&& illegal4.exec($('#uphone').val()) && ($('#uqq').val().length < 11 && $('#uqq').val().length > 4) && ($('#uwechat').val().length < 26 && $('#uwechat').val().length > 2))
			{
				$('#submit1').attr('disabled',false);
			}
			else
			{
				$('#submit1').attr('disabled',true);
			}
		}
	else
		$('#next').attr('disabled',true);
		
	/* if(illegal1.exec($('#uaccount').val())  && illegal2.exec($('#upassword').val()) && $('#upassword').val() == $('#enupassword').val() && )
		$('#submit').attr('disabled',false);
	else
		$('#submit').attr('disabled',true); */
}
function hide(){
	var email = $('#umail').val();
	var illegal3= /^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$/
	if(illegal3.exec(email)){
		$('#show_mess4').html('')
	}
}

$("#uaccount").bind("input propertychange", function () {
	regist($(this).val(),$(this).attr('id'));
});
$("#upassword").bind("input propertychange", function () {
	regist($(this).val(),$(this).attr('id'));
});
$("#enupassword").bind("input propertychange", function () {
	regist($(this).val(),$(this).attr('id'));
});
$("#umail").bind("input propertychange", function () {
	regist($(this).val(),$(this).attr('id'));
});
$("#uphone").bind("input propertychange", function () {
	regist($(this).val(),$(this).attr('id'));
});
$("#uqq").bind("input propertychange", function () {
	regist($(this).val(),$(this).attr('id'));
});
$("#uwechat").bind("input propertychange", function () {
	regist($(this).val(),$(this).attr('id'));
});