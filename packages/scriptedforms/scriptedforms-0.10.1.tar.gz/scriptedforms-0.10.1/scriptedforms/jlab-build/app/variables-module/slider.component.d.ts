import { AfterViewInit } from '@angular/core';
import { VariableBaseComponent } from './variable-base.component';
import { VariableParameterComponent } from './variable-parameter.component';
export declare class SliderComponent extends VariableBaseComponent implements AfterViewInit {
    min?: number | string;
    max?: number | string;
    step?: number | string;
    minParameter: VariableParameterComponent;
    maxParameter: VariableParameterComponent;
    stepParameter: VariableParameterComponent;
    parameterValues: {
        [s: string]: number;
    };
    setVariableParameterMap(): void;
    updateValue(value: number): void;
}
