$("#username").bind("input propertychange", function () {
				var un = $("#username").val();
				var pwd = $("#password").val();
				if(un == '')
				{
					$('#show_mess1').html('请输入用户名');
				}
				else{
					$("#show_mess1").html("");
				}
				if(un == ''||pwd== ''){
					$("#submit").attr('disabled',true);
				}
				else{
					$("#submit").attr('disabled',false);
				}
				});
			$("#password").bind("input propertychange", function () {
				var un = $("#username").val();
				var pwd = $("#password").val();
				if(pwd == '')
				{
					$('#show_mess2').html('请输入密码');
				}
				else{
					$("#show_mess2").html("");
				}
				if(un == ''||pwd== ''){
					$("#submit").attr('disabled',true);
				}
				else{
					$("#submit").attr('disabled',false);
				}
				});