/* ajax to get send mail and get response*/
$(document).ready(function(){
	logo=function(e){
		location.reload();
    };
/////////////////////////////tab change///////////////////////////////////////////////

    $('.nav.navbar-nav > li').on('click', function(e) {
        $('.nav.navbar-nav > li').removeClass('active');
        $(this).addClass('active');
    });

/////////////////////////////Mail Function////////////////////////////////////////////
	sendMessage=function(){
        //disableFunction('submitButton');
        var name = $("#name").val();
        var email = $("#email").val();
        var message = $("#message").val();
        if (name == '' || email== '' || message == ''){

            $.notify(
                "Please fill all inputs",
                {position: "top center"}
            );

            //$(".submitBtn").attr("disabled", false);



        }else {
            submitDisable();
            var formData = $('#douhavesuggestion').serializeObject();
            $.ajax({
                url:"http://127.0.0.1:8000/sendEmail/",
                method:"POST",
                data:formData,
                success:function(xhr, response, options){
                    console.log(xhr);
                    $('#douhavesuggestion')[0].reset();
                    if (xhr['result'] === 'fail') {
                      $.notify(
                        xhr['message'],
                        {position: "top center",
                         className: "error"}
                    );
                    }
                    else
                    $.notify(
                        xhr['message'],
                        {position: "top center",
                         className: "success"}
                    );
                    $(".submitBtn").attr("disabled", false);

                },
                error:function(xhr, response, options){
                    $('#douhavesuggestion')[0].reset();
                    $.notify(response, "error");
                    $(".submitBtn").attr("disabled", false);
                }
            });
        }
        //document.getElementById('submitButton').disabled = 'false';
    };

////////////////////////////////// Show hide division //////////////////////////////////
    // hides the slickbox as soon as the DOM is ready
    $('#more-info').hide();
    // shows the slickbox on clicking the noted link  
    $('#show').click(function() {
        $('#more-info').slideDown('slow');
        $("#know-more").attr("class", "hide");
        return false;
    });
    // hides the slickbox on clicking the noted link  
    $('#hide').click(function() {
        $('#more-info').slideUp('slow');
        $("#know-more").attr("class", "container text-center show");
        return false;
    });

//////////////////////////////////// Scroll Top ///////////////////////////////////////
    //Check to see if the window is top if not then display button
    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('.scrollToTop').fadeIn();
        } else {
            $('.scrollToTop').fadeOut();
        }
    });

    //click to scroll to top
    $('.scrollToTop').click(function(){
        $('html, body').animate({scrollTop : 0},800);
        return false;
    });



});

///////////////////////////////// Serialize function for ajax///////////////////////////////////////////
/*Serialize object function, included in this file only to minimize the script loading at DOM creation*/
$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

///////////////////////////lazy loading///////////////////////////////
$(function() {
    $("img.lazy").lazyload();
});

/////////////////////////disable submit button/////////////////////
submitDisable= function(){
    $(".submitBtn").attr("disabled", true);
    return true;
}



//hide results when clicked outside of search field and search exam

$("body").click(function() {
    $("#searchResults").removeClass("show").addClass("hide");
});


window.searchListIndex = -1;
$('#examName').keyup(function(e) {

    switch (e.keyCode) {
        // User pressed "up" arrow
        case 38:
            Navigate(-1);
            break;
        // User pressed "down" arrow
        case 40:
            Navigate(1);
            break;
        // User pressed "enter"
        case 13:
            if (examName.value == ''){
                //e.preventDefault();
                return false;
            } else{
                if (currentUrl != '') {
                    window.location = currentUrl;
                }
            }

            break;
        case 27:
            //$("#searchResults").hide();
            $("#searchResults").removeClass("show");
            $("#searchResults").addClass("hide");
            break;

        default:
            window.searchListIndex = -1;
            //$("#searchResults").show();
            if ($("#examName").val().length > 2){
                $("#searchResults").removeClass("hide");
                $("#searchResults").addClass("show");
                var formData = $('#search_form').serializeObject();
                $.ajax({
                    url:"/search_ajax/",
                    method:"POST",
                    data:formData,
                    success:function(xhr, response, options){

                        //$('#search_form')[0].reset();
                        $('#searchResults').html(xhr);
                        //$('#searchResults').html[0].reset();
                    },
                    error:function(xhr, response, options){
                        $('#search_form')[0].reset();
                        $('#searchResults').html(response);
                    }
                });
            }


    }

});

var Navigate = function(diff) {
    searchListIndex += diff;
    var searchList = $(".search-list");
    if (searchListIndex >= searchList.length)
        searchListIndex = 0;
    if (searchListIndex < 0)
        searchListIndex = searchList.length - 1;
    var cssClass = "search-list-hover";
    searchList.removeClass(cssClass).eq(searchListIndex).addClass(cssClass);
    var textSelect = searchList.eq(searchListIndex).text();
    $("#examName").val(textSelect);
}

/////////////////////Profile editable///////////////////////////////////
$('#editme').click(function(){

});
$("#uploadimage").on('submit',function(e)
{
    e.preventDefault();
    $(this).ajaxSubmit(

        {
            beforeSend:function()
            {
                $("#prog").show();
                $("#prog").attr('value','0');

            },
            uploadProgress:function(event,position,total,percentCompelete)
            {
                $("#prog").attr('value',percentCompelete);
                $("#percent").html(percentCompelete+'%');
            },
            success:function(data)
            {
                $("#here").html(data);
            }
        });
});


///////////////////////////////////////////////////////
$(function() {

    var $formLogin = $('#loginForm');
    var $formLost = $('#forget-password');
    var $formRegister = $('#registerWithUsForm');
    var $divForms = $('#div-forms');
    var $modalAnimateTime = 300;
    var $msgAnimateTime = 150;
    var $msgShowTime = 2000;


    $('#login_register_btn').click( function () { modalAnimate($formLogin, $formRegister) });
    $('#register_login_btn').click( function () { modalAnimate($formRegister, $formLogin); });
    $('#login_lost_btn').click( function () { modalAnimate($formLogin, $formLost); });
    $('#lost_login_btn').click( function () { modalAnimate($formLost, $formLogin); });
    $('#lost_register_btn').click( function () { modalAnimate($formLost, $formRegister); });
    $('#register_lost_btn').click( function () { modalAnimate($formRegister, $formLost); });

    function modalAnimate ($oldForm, $newForm) {
        var $oldH = $oldForm.height();
        var $newH = $newForm.height();
        $divForms.css("height",$oldH);
        $oldForm.fadeToggle($modalAnimateTime, function(){
            $divForms.animate({height: $newH}, $modalAnimateTime, function(){
                $newForm.fadeToggle($modalAnimateTime);
            });
        });
    }

    function msgFade ($msgId, $msgText) {
        $msgId.fadeOut($msgAnimateTime, function() {
            $(this).text($msgText).fadeIn($msgAnimateTime);
        });
    }

    function msgChange($divTag, $iconTag, $textTag, $divClass, $iconClass, $msgText) {
        var $msgOld = $divTag.text();
        msgFade($textTag, $msgText);
        $divTag.addClass($divClass);
        $iconTag.removeClass("glyphicon-chevron-right");
        $iconTag.addClass($iconClass + " " + $divClass);
        setTimeout(function() {
            msgFade($textTag, $msgOld);
            $divTag.removeClass($divClass);
            $iconTag.addClass("glyphicon-chevron-right");
            $iconTag.removeClass($iconClass + " " + $divClass);
  		}, $msgShowTime);
    }
});

//////////////////////////////objective exam create////////////////////
$('#')