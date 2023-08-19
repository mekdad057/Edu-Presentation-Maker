

$(document).ready(() => {
    refreshFilesList()
    
    setToastrOptions()

    addSubmitUrlListener()
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
        })
        event.preventDefault()
    })
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
    files.forEach(file => {
        const fileName = file["fileName"]
        const fileSize = file["fileSize"]
        let div = `<div id="${fileName}" class="uploader-input-element bg-white border br-4 font-size-110 position-relative local-id-0 input-status-done">
                    <div class="px-3 py-2 d-flex align-items-center justify-content-between flex-row">
                        <div class="d-inline-flex py-1 pr-4 justify-content-between flex-wrap flex-sm-nowrap flex-basis-100 flex-shrink-1 ml-n2_ mb-n2 flex-grow-1-unimportant" style="min-width: 0px;">
                            <div class="d-flex align-items-center ml-2_ mb-2 overflow-hidden"><!----> <!----> 
                                <span title="${fileName}" class="overflow-hidden text-overflow-ellipsis white-space-nowrap">${fileName}</span>
                            </div> 
                            <div class="ml-2_ mb-2 mt-n1 flex-sm-shrink-0 test">
                                <span title="File size" class="badge d-inline-flex align-items-center font-weight-normal font-size-100 bg-gray-light mt-1 mr-2_"><!----> ${fileSize} MB<!----></span>
                            </div>
                        </div> 
                        <div class="d-inline-flex align-self-baseline" style="padding-top: 0.125rem;">
                            <button title="Show more information about this file" class="btn btn-light border icon-25 p-0 mr-3 visibility-hidden">
                                <i class="far fa-info-circle"></i>
                            </button>
                            <button type="button" title="Remove file from task" class="btn btn-danger fs-4 fw-bold p-0" onclick="removeFile('${fileName}')">
                                &times;
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

function removeFile(name) {
    $.ajax({
        data : JSON.stringify({"name": name}),
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
