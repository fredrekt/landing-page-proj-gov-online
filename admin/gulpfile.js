var gulp = require('gulp');  
var sass = require('gulp-sass');  
var browserSync = require('browser-sync').create();

var paths = {
    styles: {
        src: "assets/sass/*.scss",
        dest: "assets/css"
    }
}

function style() {
    return gulp
            .src(paths.styles.src)
            .pipe(sass())
            .on("error", sass.logError)
            .pipe(gulp.dest(paths.styles.dest))
            .pipe(browserSync.stream());
}

// function reload() {
//     browserSync.reload();
// }

function watch(){
    browserSync.init({
        server: {
            baseDir: "./"
        }
    });

    gulp.watch(paths.styles.src, style);
    // gulp.watch("*.html", reload);
};

exports.watch = watch;
exports.style = style;