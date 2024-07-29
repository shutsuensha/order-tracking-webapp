window.onload = function() {
    try {
        document.getElementById('target-element').scrollIntoView({ behavior: 'smooth' });
    } catch(err) {
        console.log('error')
    }
    try {
        document.getElementById('comments').scrollIntoView({ behavior: 'smooth' });
    } catch(err) {
        console.log('error')
    }
}