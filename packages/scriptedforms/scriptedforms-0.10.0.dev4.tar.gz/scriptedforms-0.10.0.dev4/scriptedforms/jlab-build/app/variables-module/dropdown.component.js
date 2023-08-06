"use strict";
// Scripted Forms -- Making GUIs easy for everyone on your team.
// Copyright (C) 2017 Simon Biggs
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published
// by the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version (the "AGPL-3.0+").
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU Affero General Public License and the additional terms for more
// details.
// You should have received a copy of the GNU Affero General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.
// ADDITIONAL TERMS are also included as allowed by Section 7 of the GNU
// Affrero General Public License. These aditional terms are Sections 1, 5,
// 6, 7, 8, and 9 from the Apache License, Version 2.0 (the "Apache-2.0")
// where all references to the definition "License" are instead defined to
// mean the AGPL-3.0+.
// You should have received a copy of the Apache-2.0 along with this
// program. If not, see <http://www.apache.org/licenses/LICENSE-2.0>.
var core_1 = require("@angular/core");
var variable_base_component_1 = require("./variable-base.component");
var variable_parameter_component_1 = require("./variable-parameter.component");
var DropdownComponent = /** @class */ (function (_super) {
    __extends(DropdownComponent, _super);
    function DropdownComponent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.parameterValues = {
            optionsValue: []
        };
        return _this;
    }
    DropdownComponent.prototype.setVariableParameterMap = function () {
        this.variableParameterMap = [
            [this.optionsParameter, 'optionsValue'],
        ];
    };
    DropdownComponent.prototype.pythonValueReference = function () {
        var valueReference;
        if (typeof this.variableValue === 'string') {
            var escapedString = String(this.variableValue)
                .replace(/\\/g, '\\\\')
                .replace(/\"/g, '\\\"');
            valueReference = "\"\"\"" + String(escapedString) + "\"\"\"";
        }
        else {
            valueReference = String(this.variableValue);
        }
        return valueReference;
    };
    __decorate([
        core_1.Input(),
        __metadata("design:type", String)
    ], DropdownComponent.prototype, "items", void 0);
    __decorate([
        core_1.ViewChild('optionsParameter'),
        __metadata("design:type", variable_parameter_component_1.VariableParameterComponent)
    ], DropdownComponent.prototype, "optionsParameter", void 0);
    DropdownComponent = __decorate([
        core_1.Component({
            selector: 'variable-dropdown',
            template: "\n<span #variablecontainer *ngIf='variableName === undefined'>\n  <ng-content></ng-content>\n</span>\n<variable-parameter #optionsParameter *ngIf=\"items\">{{items}}</variable-parameter>\n<mat-form-field class=\"variableDropdown\">\n  <mat-label>{{labelValue}}</mat-label>\n  <mat-select class=\"variableDropdown\"\n  [required]=\"required\"\n  [disabled]=\"!isFormReady\"\n  [placeholder]=\"placeholder\"\n  [(ngModel)]=\"variableValue\"\n  (ngModelChange)=\"variableChanged($event)\"\n  (blur)=\"onBlur()\"\n  (focus)=\"onFocus()\">\n    <mat-option *ngFor=\"let option of parameterValues.optionsValue\" [value]=\"option\">{{option}}</mat-option>\n  </mat-select>\n</mat-form-field>",
            styles: [
                ".variableDropdown {\n  width: 100%;\n}\n"
            ]
        })
    ], DropdownComponent);
    return DropdownComponent;
}(variable_base_component_1.VariableBaseComponent));
exports.DropdownComponent = DropdownComponent;
//# sourceMappingURL=dropdown.component.js.map