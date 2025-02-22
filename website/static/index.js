function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function likePost(postId) {
    const likeButton = document.getElementById(`like-button-${postId}`);
    const likeIcon = likeButton.querySelector('i');
    const likeCount = document.getElementById(`like-count-${postId}`);

    fetch(`/like-post/${postId}`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.liked) {
            likeIcon.classList.replace('far', 'fas');
        } else {
            likeIcon.classList.replace('fas', 'far');
        }
        likeCount.innerHTML = data.likes;
    })
    .catch(() => {
        console.error('Error liking post');
        alert("Could not like post");
    });
}