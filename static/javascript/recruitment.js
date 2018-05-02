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

$(document).ready(function() {
  //the following variables and list of objects is used as testing cases.
  var nameOfStudy, description, researcher, contact;
  var content = [{
    nameOfStudy: "Study 1",
    description: "Participants must be X",
    researcher: "Dr. John Smith",
    contact: "johnsmith1st@gmail.com"
  }, {
    nameOfStudy: "Study 2",
    description: "Participants must be Y",
    researcher: "Dr. Jane Doe",
    contact: "jjaned@gmail.com"
  }, {
    nameOfStudy: "Study 3",
    description: "Participants must be z",
    researcher: "Dr. Teddy Colon",
    contact: "ted.colon@burke.com"
  }];
  /*This function takes a list of objects and runs each object through another
  function called "genAccordionContent" which generates HTML for accordion based
  on Study information provided in the object (keys and values). The HTML for
  the accordion is then appended to the parent div "#accordion"*/
  content.forEach(function(elem) {
    $('#accordion').append(genAccordContent(elem));
  });
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
  var headers, leftModalContainer, temp, footer, testContent, obj, questions, rightModalContainer;
  var title, description, researcher_name, researcher_email;
  //headers titles for the left column of the modal
  headers = {
    "Title of Study": "title",
    "Description": "description",
    "Name of Researcher(s)": "researcher_name",
    "Contact Information": "researcher_email"
  };
  leftModalContainer = [];

  //generating the left container for the modal and compiling them to a list
  for (ind in headers) {
    temp = '<h5 style="padding-left:10px;">' + ind + '</h5>';
    if (ind === "Description") {
      temp += '<textarea class="full-width" cols="40"  rows="5" style="resize:none; overflow:auto; margin:0 0 5px 10px;"></textarea>';
    } else {
      temp += '<input class="full-width" type="text" name=' + headers[ind] + ' style="margin: 0 0 5px 10px;" required>';
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
  rightModalContainer = "<h5 style='padding-top:10px;'>Filter By:</h5><div class='right-nstudy' style='position:relative'><div class='col-sm-6'>" + questions + "</div></div>";

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
      val3 = genModalContent()[2];
    parentDivId.append(modalHtml);
    val1.forEach(function(val) {
      $('.lns').append(val);
    });
    $('.lns').after(val3);
    $('.add-study-content').append(val2);
    $('.study-footer').append('<button type="submit" class="btn btn-default">Create</button>\
    <button type="button" class="close-modbtn btn btn-default">Close</button>');
    $('.close-modbtn').on("click", function() {
      $('#pop-up-modal').remove();
      $('.modal-backdrop').remove();
    });
  }
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
    if (ind == "nameOfStudy") {

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
        checkbox_input = '<input class="pancheck" type="checkbox" name="studs">';

      // panel heading
      var open_panel_header = '<div class="panel-heading collapsed" data-toggle="collapse" data-target=#' + unID + ' style="background-color:#337ab7 !important;">';

      //title html
      tempTitle += open_panel_header + open_header5_tag + open_panel_div + checkbox_input +
        close_div + open_anchor_tag + objt[ind] + close_anchor + close_header5_tag + close_div;

    } else if (ind == "description") {

      //description html

      tempDesc += open_header6_tag + ind.toUpperCase() + ":" + close_header6_tag + open_para_tag +
        objt[ind] + close_para_tag;

    } else if (ind == "researcher") {

      //researcher name html

      tempReschr += open_header6_tag + ind.toUpperCase() + ":" + close_header6_tag + open_para_tag +
        objt[ind] + close_para_tag;

    } else if (ind == "contact") {

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