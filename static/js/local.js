$('#province').change(function(){
    var proIndex=$("#province").get(0).selectedIndex-1
    $('#province').removeClass('select-warning')
    $("#citys").empty()
    $("#area").empty()
    $('#citys').append("<option value='no' selected disabled>-=城市或地区=-</option>")
    for(j=0;j<local[proIndex].city.length;j++)
    {
        $('#citys').append("<option value="+local[proIndex].city[j].name+">"+local[proIndex].city[j].name+"</option>")
    }
})
$('#citys').change(function(){
    var proIndex=$("#province").get(0).selectedIndex-1
    var citysIndex=$("#citys").get(0).selectedIndex-1
    $('#citys').removeClass('select-warning')
    $("#area").empty()
    $('#area').append("<option value='no' selected disabled>-=区/县=-</option>")
    for(k=0;k<local[proIndex].city[citysIndex].area.length;k++)
    {
        $('#area').append("<option value="+local[proIndex].city[citysIndex].area[k]+">"+local[proIndex].city[citysIndex].area[k]+"</option>")
    }
})
$('#area').change(function(){
    $('#area').removeClass('select-warning')
})
$('#country').click(function(){
    var val = $(this).val()
    if(val == '中国')
    {
        $('#China_show').removeClass('message_hidden')
        $('#Other_show').addClass('message_hidden')
    }
    else
    {
        $('#China_show').addClass('message_hidden')
        $('#Other_show').removeClass('message_hidden')
    }
});