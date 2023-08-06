import {addTupleType, Tuple} from "@synerty/vortexjs";
import {tutorialTuplePrefix} from "../PluginNames";


@addTupleType
export class TutorialTuple extends Tuple {
    public static readonly tupleName = tutorialTuplePrefix + "TutorialTuple";

    //  Description of date1
    dict1 : {};

    //  Description of array1
    array1 : any[];

    //  Description of date1
    date1 : Date;

    constructor() {
        super(TutorialTuple.tupleName)
    }
}