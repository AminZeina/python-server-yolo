let homepage = {
    setup: function () {
        homepage.imageUrl = "http://localhost:8080/latest-image"
        homepage.droneImage = $('#droneImage')
        homepage.refreshing = false
        $(document).on('click', '#toggleRefreshButton', homepage.toggleRefreshing);
    },
    toggleRefreshing: function () {
        console.log('start')
        let button = $('#toggleRefreshButton')
        if (button.attr('value') == 'start') {
            // Start refreshing image, every 2 seconds
            this.refreshId = setInterval(homepage.refreshImage, 2000)
            button.html('Stop refreshing image').prop('value', 'stop')
        } else {
            clearInterval(this.refreshId)
            button.html('Start refreshing image').prop('value', 'start')
        }
        
    },
    refreshImage: function () {
        homepage.droneImage.attr('src', 'http://localhost:8080/latest-image?' + new Date().getTime())

    }
}

$(homepage.setup)