import { Widget } from '@phosphor/widgets';
import { PromiseDelegate } from '@phosphor/coreutils';
import { Type, ComponentRef, NgZone } from '@angular/core';
export declare class AngularLoader<M> {
    private applicationRef;
    private componentFactoryResolver;
    ngZone: NgZone;
    private injector;
    loaderReady: PromiseDelegate<void>;
    constructor(ngModule: Type<M>);
    attachComponent<T>(ngComponent: Type<T>, dom: Element): Promise<ComponentRef<T>>;
}
export declare class AngularWidget<C, M> extends Widget {
    ngZone: NgZone;
    componentRef: ComponentRef<C>;
    componentInstance: C;
    componentReady: PromiseDelegate<void>;
    constructor(ngComponent: Type<C>, angularLoader: AngularLoader<M>, options?: Widget.IOptions);
    run(func: () => void): void;
    dispose(): void;
}
