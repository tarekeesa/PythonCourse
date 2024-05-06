$(document).ready(function() {
    console.log("Document ready!");
    $('#commentForm').submit(function(e) {
        e.preventDefault();
        console.log("Form submission intercepted.");
        var formData = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            success: function(response) {
                var newCommentHtml = `
                    <div class="d-flex">
                        <img src="img/avatar.jpg" class="img-fluid rounded-circle p-3" style="width: 100px; height: 100px;" alt="">
                        <div class="">
                            <p class="mb-2" style="font-size: 14px;">${new Date().toLocaleDateString()}</p>
                            <div class="d-flex justify-content-between">
                                <h5>${response.username}</h5>
                                <div class="d-flex mb-3">
                                    <!-- Placeholder for star ratings if needed -->
                                    <i class="fa fa-star text-secondary"></i>
                                    <i class="fa fa-star text-secondary"></i>
                                    <i class="fa fa-star text-secondary"></i>
                                    <i class="fa fa-star text-secondary"></i>
                                    <i class="fa fa-star"></i>
                                </div>
                            </div>
                            <p>${response.content}</p>
                        </div>
                    </div>
                `;
            
                $('#reviewsContainer').prepend(newCommentHtml);  // Append the new comment at the top of the reviews container
                $('#commentForm')[0].reset();  // Reset the form fields after successful submission
            },
            error: function(xhr, status, error) {
                console.error("Error posting comment:", error);
            }
        });
    });
});
