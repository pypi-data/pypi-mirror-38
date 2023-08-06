import { JupyterLabPlugin } from '@jupyterlab/application';
import { ABCWidgetFactory, DocumentRegistry } from '@jupyterlab/docregistry';
import { ServiceManager, ContentsManager } from '@jupyterlab/services';
import { AngularLoader } from '../app/phosphor-angular-loader';
import { AppModule } from '../app/app.module';
import { ScriptedFormsWidget } from './../app/widget';
export declare namespace IScriptedFormsWidgetFactory {
    interface IOptions extends DocumentRegistry.IWidgetFactoryOptions {
        serviceManager: ServiceManager;
        contentsManager: ContentsManager;
        angularLoader: AngularLoader<AppModule>;
    }
}
export declare class ScriptedFormsWidgetFactory extends ABCWidgetFactory<ScriptedFormsWidget, DocumentRegistry.IModel> {
    serviceManager: ServiceManager;
    contentsManager: ContentsManager;
    angularLoader: AngularLoader<AppModule>;
    constructor(options: IScriptedFormsWidgetFactory.IOptions);
    protected createNewWidget(context: DocumentRegistry.Context): ScriptedFormsWidget;
}
export declare const plugin: JupyterLabPlugin<void>;
