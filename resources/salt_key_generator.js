if (process.argv.length < 3) {
    console.error("A number is required in argument for the length");
    process.exit(1);
}

let allowed_elements = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/-*~#$=%:@(){}[]"

let n = 0;
try {
    let l_given = Number(process.argv[2])
    if (isNaN(l_given)) {
        console.error("You didn't gave a number for the length");
        process.exit(1);
    } else {
        n = l_given;
    }
} catch (e){
    console.error(e)
    console.error("You didn't gave a number for the length");
    process.exit(1);
}

for (let i = 0; i < n; i++) {
    process.stdout.write(allowed_elements[Math.floor(Math.random() * allowed_elements.length)]);
}