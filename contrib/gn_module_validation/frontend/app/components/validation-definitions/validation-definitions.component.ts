import { Component, OnInit } from "@angular/core";
import { ValidationDataService } from "../../services/data.service";
import { CommonService } from "@geonature_common/service/common.service";

import { ConfigService } from "@geonature/utils/configModule/core";

@Component({
  selector: "pnx-validation-definitions",
  templateUrl: "validation-definitions.component.html",
  styleUrls: ["./validation-definitions.component.scss"],
  providers: []
})
export class ValidationDefinitionsComponent implements OnInit {
  public definitions;
  public VALIDATION_CONFIG: any;
  private showDefinitions: Boolean = false;

  constructor(
    public searchService: ValidationDataService,
    private _commonService: CommonService,
    private _configService: ConfigService
  ) {}
  ngOnInit() {
    this.VALIDATION_CONFIG = this._configService.getSettings("VALIDATION");
  }

  getDefinitions(param) {
    this.showDefinitions = !this.showDefinitions;
    this.searchService.getDefinitionData().subscribe(
      result => {
        this.definitions = result;
      },
      error => {
        if (error.statusText === "Unknown Error") {
          // show error message if no connexion
          this._commonService.translateToaster(
            "error",
            "ERROR: IMPOSSIBLE TO CONNECT TO SERVER"
          );
        } else {
          // show error message if other server error
          this._commonService.translateToaster("error", error.error);
        }
      }
    );
  }
}
