import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";

import { ConfigService } from "@geonature/utils/configModule/core";

@Injectable()
export class OcctaxDataService {
  public readonly ABSOLUTE_MODULE_URL: string;
  constructor(private _api: HttpClient, private _configService: ConfigService) {
    this.ABSOLUTE_MODULE_URL =
      this._configService.getSettings("API_ENDPOINT") +
      "/" +
      this._configService.getSettings("OCCTAX.MODULE_URL");
  }

  getOneReleve(id) {
    return this._api.get<any>(`${this.ABSOLUTE_MODULE_URL}/releve/${id}`);
  }

  deleteReleve(id) {
    return this._api.delete(`${this.ABSOLUTE_MODULE_URL}/releve/${id}`);
  }

  postOcctax(form) {
    return this._api.post(`${this.ABSOLUTE_MODULE_URL}/releve`, form);
  }

  getOneCounting(id_counting) {
    return this._api.get<any>(
      `${this.ABSOLUTE_MODULE_URL}/counting/${id_counting}`
    );
  }
}
