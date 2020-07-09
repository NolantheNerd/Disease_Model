// Define a Function Similar to the random.sample function from the Python Default Library
function sample(population, k){
    /*
        Chooses k unique random elements from a population sequence or set.

        Returns a new list containing elements from the population while
        leaving the original population unchanged.  The resulting list is
        in selection order so that all sub-slices will also be valid random
        samples.  This allows raffle winners (the sample) to be partitioned
        into grand prize and second place winners (the subslices).

        Members of the population need not be hashable or unique.  If the
        population contains repeats, then each occurrence is a possible
        selection in the sample.

        To choose a sample in a range of integers, use range as an argument.
        This is especially fast and space efficient for sampling from a
        large population:   sample(range(10000000), 60)

        Sampling without replacement entails tracking either potential
        selections (the pool) in a list or previous selections in a set.

        When the number of selections is small compared to the
        population, then tracking selections is efficient, requiring
        only a small set and an occasional reselection.  For
        a larger number of selections, the pool tracking method is
        preferred since the list takes less space than the
        set and it doesn't suffer from frequent reselections.
    */

    if(!Array.isArray(population))
        throw new TypeError("Population must be an array.");
    var n = population.length;
    if(k < 0 || k > n)
        throw new RangeError("Sample larger than population or is negative");

    var result = new Array(k);
    var setsize = 21;   // size of a small set minus size of an empty list

    if(k > 5)
        setsize += Math.pow(4, Math.ceil(Math.log(k * 3, 4)))

    if(n <= setsize){
        // An n-length list is smaller than a k-length set
        var pool = population.slice();
        for(var i = 0; i < k; i++){          // invariant:  non-selected at [0,n-i)
            var j = Math.random() * (n - i) | 0;
            result[i] = pool[j];
            pool[j] = pool[n - i - 1];       // move non-selected item into vacancy
        }
    }else{
        var selected = new Set();
        for(var i = 0; i < k; i++){
            var j = Math.random() * n | 0;
            while(selected.has(j)){
                j = Math.random() * n | 0;
            }
            selected.add(j);
            result[i] = population[j];
        }
    }

    return result;
}


class Society {
    constructor(pop, n_reg, pirt, tf, pi, pac, ttr, incp, dr, psd, quar, qd, cl, vf, sdd) {
        // Monitor the State of the Society
        this.ongoing = true;
        
        // Store Society Specific Information
        this.n_reg = n_reg;
        this.pirt = pirt/100;
        this.sdd = sdd;
        this.incp = incp;
        this.quar = quar;
        this.qd = qd;
        
        this.travel_permitted = true;
        this.social_distancing = false;
        
        // Person Object List - This is where all the Person Objects live
        // (Start with null so id == list index as id starts at 1)
        this.people = [null];
        
        // Prepare lists for different types of people - These lists only hold Person IDs
        this.healthy = new math.Range(2, pop + 1).toArray();
        this.asympt = [1];
        this.sympt = [];
        this.recovered = [];
        this.dead = [];
        this.traveling = [];
        this.shopping = [];
        this.will_social_distance = sample(new math.Range(1, pop + 1).toArray(), psd/100*pop);
    }
}

console.log("Derp")

var x = new Society(100, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0)