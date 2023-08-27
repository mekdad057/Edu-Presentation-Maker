

$(document).ready(() => {

    refreshFilesList()
    
    setToastrOptions()

    addSubmitUrlListener()

    refreshControlBtns()
})

function setToastrOptions() {
    //Command: toastr["success"]("URL added successfully")
    toastr.options = {
        "closeButton": false,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-top-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }
}

function addSubmitUrlListener() {
    
    $('#addRemoteUrlForm').on('submit',(event)=>{
        _url = $("#remoteUrlInput").val();
        $.ajax({
            data : JSON.stringify({"url": _url}),
            contentType: "application/json",
            type : "POST",
            url : "/add-url",
            success: (res) => {
                if (res.success) {
                    toastr["success"]("URL added successfully")
                    console.log(res)
                    refreshFilesList(res.filesList)
                } else {
                    console.log(res)
                    toastr["error"](res.message)
                }
            },
            error: (msg) => {
                console.log(msg)
            }
        });
        event.preventDefault()
    });

    $("#createPresentationForm").on("submit", (event) => {
        event.preventDefault();

        startCreatingPresentation();
        
    });
}

async function refreshFilesList(files = null) { 
    if (files == null) {
        files = await $.get("/get-files", {}, (res) =>{
            if (res.success) {
                return res.filesList
            }
            else {
                console.log(res.message);
            }
        },
        "json"
        );
    }

    $("#filesList").empty()
    if (files.length != 0) {
        $("#filesList").append(`<div class="flex-row mb-2">
                                    <div class="col-12-lg">
                                        <button type="button" class="btn btn-danger" onclick="removeAllFiles()">
                                            <span class="px-4 py-2">remove all</span>
                                        </button>
                                    </div>
                                </div>`)
    };
    files.forEach(file => {
        const url = file
        let div = `<div id="${url}" class="uploader-input-element bg-white border br-4 font-size-110 position-relative local-id-0 input-status-done mb-1">
                    <div class="px-3 py-2 d-flex align-items-center justify-content-between flex-row">
                        <div class="d-inline-flex py-1 pr-4 justify-content-between flex-wrap flex-sm-nowrap flex-basis-100 flex-shrink-1 ml-n2_ mb-n2 flex-grow-1-unimportant" style="min-width: 0px;">
                            <div class="d-flex align-items-center ml-2_ mb-2 overflow-hidden"><!----> <!----> 
                                <span title="${url}" class="overflow-hidden text-overflow-ellipsis white-space-nowrap">${url}</span>
                            </div> 
                            <div class="ml-2_ mb-2 mt-n1 flex-sm-shrink-0 test">
                                <span title="File size" class="badge d-inline-flex align-items-center font-weight-normal font-size-100 bg-gray-light mt-1 mr-2_"><!----> html <!----></span>
                            </div>
                        </div> 
                        <div class="d-inline-flex align-self-baseline" style="padding-top: 0.125rem;">
                            <button title="Show more information about this file" class="btn btn-light border icon-25 p-0 mr-3 visibility-hidden">
                                <i class="far fa-info-circle"></i>
                            </button>
                            <button type="button" title="Remove file from task" class="btn btn-danger fs-4 fw-bold p-0" onclick="removeFile('${url}')">
                                <span class="p-2">remove</span>
                            </button>
                        </div>
                    </div> <!----> <!----> 
                    <div class="p-0 w-100 left-0 bottom-0 position-absolute overflow-hidden br-4 rounded-top-0 bg-cheap-white border-top" style="height: 4px;">
                        <div class="progress-bar h-100 bg-success" style="width: 100%;">
                        </div>
                    </div>
                </div>`;

        $("#filesList").append(div)
    
    });
    
}

function removeFile(url) {
    $.ajax({
        data : JSON.stringify({"url": url}),
        contentType: "application/json",
        type : "POST",
        url : "/remove-url",
        success: (res) => {
            if (res.success) {
                toastr["success"]("URL removed successfully")
                refreshFilesList(res.filesList)
            } else {
                console.log(res)
                toastr["error"](res.message)
            }
        },
        error: (msg) => {
            console.log(msg)
        }
    })
    
}


function removeAllFiles() {
    $.ajax({
        type: "POST",
        url: "/remove-all-files",
        success: (res) =>{
            if (res.success) {
                toastr["success"]("URLs removed successfully")
                $("#filesList").empty()
            }
            else {
                toastr["error"](res.message)
                refreshFilesList()
            }
        },
        error: (msg) => {
            console.log(msg)
        }
    });

    
}

function startCreatingPresentation() {
    progressUnit = 9 // in seconds
    updateProgress(progressUnit)
    const progressId = setInterval(() => updateProgress(progressUnit), progressUnit*1000);
    let title = $("#presentationTitle").val();
    let presentationType = $("input[name='presentationType']:checked").val();
    $.ajax({
        data: JSON.stringify({"title": title, "presentationType": presentationType}),
        url: "/create-presentation",
        type: "POST",
        contentType: "application/json",
        success: (res) => {
            if (res.success) {
                toastr["success"]("Presentation created successfully")
                $("#downloadBtn").show()
                $("#clearBtn").show()
                $("#startBtn").toggleClass("btn-primary")
                $("#startBtn").toggleClass("btn-success")
                $("#startBtnText").text("Start")
                clearInterval(progressId)
            }
            else {
                toastr["error"](res.message)
            }
        },
        error: (msg) => {
            console.log(msg)
        }
    });
}

function updateProgress(progressUnit) {
    console.log("Updating Now")
    if ($("#startBtnText").text() == "Start"){
        $("#startBtnText").text("0%")
    }
    if ($("#startBtn").hasClass("btn-success")){
        $("#startBtn").removeClass("btn-success")
        $("#startBtn").addClass("btn-primary")
    }
    const filesToProgressTotalTime = ($("#filesList").children().length-1) * 4.5*60.0 // 5 min per file/url
    let progressPercentage = $("#startBtnText").text()
    let progressValue = parseFloat(progressPercentage.replace("%",""))/100.0
    let progressTimeValue = progressValue*filesToProgressTotalTime/0.99
    if(progressTimeValue < filesToProgressTotalTime){
        progressTimeValue += progressUnit
    }
    else {
        progressTimeValue = filesToProgressTotalTime
    }
    progressValue = 0.99*progressTimeValue/filesToProgressTotalTime
    progressPercentage = (progressValue * 100).toFixed(2) + "%";
    $("#startBtnText").text(progressPercentage)

}


function clearAll() {
    removeAllFiles()
    $("#presentationTitle").val = ""
    $("#remoteUrlInput").val = ""
    $("#downloadBtn").hide()
    $("#clearBtn").hide()
}

function refreshControlBtns() {
    let fileName = ""
    $.ajax({
        url: "/get-file-name",
        type: 'GET',
        dataType: 'application/json',
        success: function(res) {
                fileName = res.fileName
                if(fileName != ""){
                    $("#downloadBtn").show()
                    $("#clearBtn").show()
                }
                else {
                    $("#downloadBtn").hide()
                    $("#clearBtn").hide()
                }
            },
        error: (msg) => {
            console.log(msg)
            }
        });
    console.log(fileName)
   

}