$(window).load(function(){
        // add next button to all screens but not last
        $("article:not(:last)").append('<a class="btn btn-primary btn-lg btn-block next" id="next-btn" href="#">Next</a>');
        //$("article:not(:first)").append('<a class="btn btn-primary btn-lg btn-block next" id="prev-btn" href="#">Previous</a>');
        //hide every form section except first
        $("article:nth-child(1n+2)").hide();
        //add class of visible to first screen
        $("article:first").addClass("visible");
        //add an empty unordered list to be populated below
        $("#objective-exam-create-form").append("<ul id='page'></ul>");
       
        //start the index at 1    
        var pageNum = 1;
        var currentPage=1;
        //go through each section (article) and add a list item to the empty unorderd list with the page number            
/*        $("article").each(function(){
            $(this).parent().find("ul").append('<li class ="pagetab" id="pagetab_'+pageNum+'"><a href="#">Page: '+pageNum+'</a></li>');
            $(this).addClass("page" + pageNum);
            pageNum++;
        });
        $('#page > li').hide();
*/
        //each time the user clicks the next button, remove the visible class, hide that section, fade in the next with a new class of visible
        $("a.next").on("click", function(e){
            var name = $("#name").val();
            var mailid = $("#mailid").val();
            var ExamName= $("#examname").val();
            var PhoneNum = $("#phonenumber").val();


            if(name =='' || mailid =='' || ExamName ==''|| PhoneNum =='') {
                $("#errormsg").html("Please fill all the value");
                $("#errormsg").attr("class", "show text-center warning-msg");
                return false
            } else{
                if (validateMailId(mailid) && validatePhoneNumber(PhoneNum)){
                    e.preventDefault();
                    $(this).closest("article").removeClass("visible").hide().next().addClass("visible").fadeIn();
                    currentPage++;
                    showCurrentTab();
                }else {
                    if(!validatePhoneNumber(PhoneNum)){
                        $("#errormsg").html("Please provide the valid phone number");

                    }else if(!validateMailId(mailid)){
                        $("#errormsg").html("Please provide the valid email id");
                    }

                    $("#errormsg").attr("class", "show text-center warning-msg");
                    return false
                }

            }

        })

        /*$("a.previous").on("click", function(e){
            e.preventDefault();
            $(this).closest("article").removeClass("visible").hide().prev().addClass("visible").fadeIn();
        })*/;

function showCurrentTab(){
 $('.pagetab').hide();
            $('#pagetab_'+currentPage).show();
}

showCurrentTab();  //Show the first tab

});

////////////////////validate phone number///////////
function validatePhoneNumber(phoneNum) {
    var phoneno = /[0-9]|\./;
    if((phoneno.test(phoneNum))){
        return true;
    }return false;
}
///////////////////validate mail id////////////////
function validateMailId(mailid){
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (mailformat.test(mailid)){
        return true;
    } return false;
}

