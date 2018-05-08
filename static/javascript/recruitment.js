$(document).ready(function() {
  $('.search').on('keyup', function() {
    var searchTerm = $(this).val().toLowerCase();
    $('#usrTable1 tbody tr').each(function() {
      var lineStr = $(this).text().toLowerCase();
      if (lineStr.indexOf(searchTerm) === -1) {
        $(this).hide();
      } else {
        $(this).show();
      }
    });
  });
});

/*This section of code should be moved because every time the page is refreshed,
this is what will appear in the accordion by default
*/

var nameOfStudy, description, researcher, contact;
var content = [{
  title: "Study for patients with recent brain injuries",
  description: "This is information about a study meant for patients who have experienced a brain injury in the last 6 months...",
  researcher_name: "Dr. John Smith",
  researcher_email: "jsmith@med.cornell.edu"
}, {
  title: "Therapy program Concussion Management",
  description: "At Burke, we have dedicated physical therapists with advanced training and experience in concussion management...",
  researcher_name: "Dr. Jane Doe",
  researcher_email: "jjane@med.cornell.edu"
}, {
  title: "Clinical trials for people with Alzheimers",
  description: "There's a new drug being tested on patients like you...",
  researcher_name: "Dr. Dylan Edwards",
  researcher_email: "dje2002@med.cornell.edu"
}];
//the following variables and list of objects is used as testing cases.

/*This function takes a list of objects and runs each object through another
function called "genAccordionContent" which generates HTML for accordion based
on Study information provided in the object (keys and values). The HTML for
the accordion is then appended to the parent div "#accordion"*/

//Note: need to adjust input text for the title text box to allow users to input different types of characters because
//...currently the title can't take in colon and apostrophes. I think this is due to the unID generation in genAccordContent(obt)...
// or some other manaipulation on the title text?
content.forEach(function(elem) {
  $('#accordion').append(genAccordContent(elem));
});

function Check(name) {
  var items = document.getElementsByName(name);
  for (var i = 0; i < items.length; i++) {
    if (items[i].type == 'checkbox') {
      if (items[i].checked == false) {
        items[i].checked = true;
      } else {
        items[i].checked = false;
      }
    }
  }
}

function genModalContent() {
  var headers, leftModalContainer, temp = '',
    footer, testContent, obj, questions, rightModalContainer;
  var title, description, researcher_name, researcher_email;
  //headers titles for the left column of the modal
  headers = {
    "Title": "title",
    "Description": "description",
    "Name of researcher": "researcher_name",
    "Contact email": "researcher_email"
  };
  leftModalContainer = [];

  //generating the left container for the modal and compiling them to a list
  for (ind in headers) {
    if (headers[ind] == "description") {
      temp = '<h5 style="padding-left:2px;">' + ind + ":" + '</h5>';
      temp += '<textarea id=' + headers[ind] + ' class="full-width" cols="40"  rows="5" name=' + headers[ind] + ' style="resize:none; overflow:auto; margin:0 0 5px;" maxlength="500" placeholder="Summary description"></textarea>';
    } else {
      if (headers[ind] == "title") {
        temp = '<h5 style="padding-left:2px;">' + ind + ":" + '</h5>';
        temp += '<input id=' + headers[ind] + ' class="full-width" type="text" name=' + headers[ind] + ' style=": margin: 0 0 5px 10px;" required="required" maxlength="50" placeholder="Header information">';
      } else if (headers[ind] == "researcher_name") {
        temp = '<h5 style="padding-left:2px;margin-top:0px;">' + ind + ":" + '</h5>';
        temp += '<input id=' + headers[ind] + ' type="text" name=' + headers[ind] + ' style="margin: 0 0 5px;width:75%;" required="required" autocomplete="name" maxlength="25" placeholder="Full name">';
      } else if (headers[ind] == "researcher_email") {
        temp = '<h5 style="padding-left:2px;">' + ind + ":" + '</h5>';
        temp += '<input id=' + headers[ind] + ' type="text" name=' + headers[ind] + ' style="margin: 0 0 10px;width:75%;" required="required" type="email" autocomplete="email" maxlength="30" placeholder="Email of researcher">';
      }
    }
    leftModalContainer.push(temp);
  }

  //generating the right container of filtering questions
  testContent = $('meta[name="question-data"]').attr('content');
  obj = JSON.parse(testContent);
  questions = "";
  for (ind in obj) {
    questions += "<div style='position:relative; height: 75px'>" + genQuestion(obj[ind]) + "</div>";
  }
  rightModalContainer = "<div class='right-nstudy' style='position:relative'><h5 style='padding-top:10px;width:50%;float:right;margin-top:0px;padding-left:10px;'>Filter By:</h5><div class='col-sm-6'>" + questions + "</div></div>";

  //footer
  footer = '<div class="modal-footer study-footer"></div>';
  return [leftModalContainer, footer, rightModalContainer];
}

function genStudyModal() {
  var parentDivId, modalHtml;
  parentDivId = $('#StudyModal');
  modalHtml = $(
    '<div class="modal fade in" id="pop-up-modal" role="dialog">\
  <div class="modal-dialog">\
  <div class="modal-content add-study-content"><div class="container" style="width:inherit;">\
  <div class="row"><div class="left-nstudy"><div class="col-sm-6 lns">\
  </div></div></div></div></div></div></div>'
  );
  if (document.getElementById('pop-up-modal') == null) {

    var val1 = genModalContent()[0],
      val2 = genModalContent()[1],
      val3 = genModalContent()[2],
      bulkForForm = '';
    parentDivId.append(modalHtml);
    val1.forEach(function(val, indx, lst) {
      bulkForForm += val;
      if (indx == (lst.length - 1)) {
        $('.lns').append('<form method="POST" id="study-form">' + bulkForForm + '</form>');
      }
    });

    $('.lns').after(val3);
    $('.add-study-content').append(val2);
    $('.study-footer').append('<input type="submit" id="create-btn" value="Create" class="btn btn-default"></input>\
    <input type="button" class="close-modbtn btn btn-default" value="Close"></input>');

    // var studyContentToPost = {
    //   nameOfStudy: $title,
    //   description: $description,
    //   researcher: $researcher_name,
    //   contact: $researcher_email
    // }

    //   var csrf_token = $('meta[name="csrf-token"]').attr('content')
    //   data += ('&cohort_num=' + '1');
    //   data += ('&csrfmiddlewaretoken=' + csrf_token);
    //
    //   $.ajax({
    //     url: '',
    //     type: 'POST',
    //     dataType: 'json',
    //     data: {
    //       title: $("#title").val(),
    //       description: $("#description").val(),
    //       researcher_name: $("#researcher_name").val(),
    //       researcher_email: $("#researcher_email").val(),
    //     },
    //     success: function(res) {
    //       alert("Success!");
    //     }
    //   });
    // });

    //create button clicked
    $("#create-btn").on("click", function(e) {
      e.preventDefault();
      var $form = $("#study-form");
      console.log("form submitted!")
      create_post();
    });

    //close button clicked
    $('.close-modbtn').on("click", function() {
      $('#pop-up-modal').remove();
      $('.modal-backdrop').remove();
    });
  }
}

function create_post() {
  console.log("function: create_post() --> disregard the following..."); //sanity check

  var data = {
    title: $("#title").val(),
    description: $("#description").val(),
    researcher_name: $("#researcher_name").val(),
    researcher_email: $("#researcher_email").val(),
  };
  data = JSON.stringify(data);
  var csrf_token = $('meta[name="csrf-token"]').attr('content')
  data += ('&cohort_num=' + '1');
  data += ('&csrfmiddlewaretoken=' + csrf_token);

  $.ajax({
    url: "",
    type: "POST",
    dataType: "json",
    data: data,
    success: function(json) {
      content.push(json);
      $('#accordion').append(genAccordContent(json));
      $('#pop-up-modal').remove();
      $('.modal-backdrop').remove();
    }
  });
}

function genAccordContent(objt) {
  //function should take in a JSON object
  // thus, consider: objt = JSON.parse(objt) when taking object from backend
  var encap_all = '<div class="panel panel-default">',
    open_para_tag = '<p>',
    close_para_tag = '</p>',
    open_header6_tag = '<h6>',
    close_header6_tag = '</h6>',
    close_div = '</div>',
    unID = '',
    tempTitle = '',
    tempDesc = '',
    tempReschr = '',
    contactInfo = '';

  for (ind in objt) {
    if (ind == "title") {

      //panel div for input
      var open_panel_div = '<div class="pancheck" style="display:inline;">';

      //Header5 tags for header div
      var open_header5_tag = '<h5 class="panel-title">',
        close_header5_tag = '</h5>';

      //generating pseudo-unique id as a place holder based on the title of the study
      unID += objt[ind].substring(Math.ceil((objt[ind].length) / 3), objt[ind].length);
      unID = unID.replace(/\s/g, "-");

      //anchoring tags
      var open_anchor_tag = '<a class="accordion-toggle" data-parent="#accordion" href=#' + unID + ' style="padding-left:10px;color: #fff !important;">',
        close_anchor = '</a>',
        checkbox_input = '<input class="pancheck" type="checkbox" name="studs">',
        open_remove_icon_div = '<div class="glyphicon glyphicon-remove" style="float:right;right:40px;background-color:#337ab7 !important">';

      // panel heading
      var open_panel_header = '<div class="panel-heading collapsed" data-toggle="collapse" data-target=#' + unID + ' style="background-color:#337ab7 !important;">';

      //title html
      tempTitle += open_panel_header + open_header5_tag + open_panel_div + checkbox_input +
        close_div + open_anchor_tag + objt[ind] + open_remove_icon_div + close_div + close_anchor + close_header5_tag + close_div;

    } else if (ind == "description") {

      //description html

      tempDesc += open_header6_tag + ind.toUpperCase() + ":" + close_header6_tag + open_para_tag +
        objt[ind] + close_para_tag;

    } else if (ind == "researcher_name") {

      //researcher name html

      tempReschr += open_header6_tag + ind.toUpperCase() + ":" + close_header6_tag + open_para_tag +
        objt[ind] + close_para_tag;

    } else if (ind == "researcher_email") {

      //contact html

      contactInfo += open_header6_tag + ind.toUpperCase() + ":" + close_header6_tag + open_para_tag +
        objt[ind] + close_para_tag;
    }
  }

  if (unID.length > 0) {
    var accord_hidden_div = '<div id="' + unID + '" class="panel-collapse collapse" aria-expanded="false">';
    var open_panel_body = '<div class="panel-body">';
    var accordBody = encap_all + tempTitle + accord_hidden_div + open_panel_body + tempDesc + tempReschr + contactInfo + close_div + close_div + close_div;
    return accordBody;
  } else {
    throw "Function does not contain a unique ID greater than 0";
  }
}