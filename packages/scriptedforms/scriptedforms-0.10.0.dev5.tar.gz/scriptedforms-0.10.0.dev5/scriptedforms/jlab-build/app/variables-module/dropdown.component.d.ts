import { AfterViewInit } from '@angular/core';
import { VariableBaseComponent } from './variable-base.component';
import { VariableParameterComponent } from './variable-parameter.component';
export declare class DropdownComponent extends VariableBaseComponent implements AfterViewInit {
    items: string;
    optionsParameter: VariableParameterComponent;
    parameterValues: {
        [s: string]: (string | number)[];
    };
    setVariableParameterMap(): void;
    pythonValueReference(): string;
}
