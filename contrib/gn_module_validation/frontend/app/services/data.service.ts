import { Injectable } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { isArray } from "util";
import { ConfigService } from "@geonature/utils/configModule/core";

@Injectable()
export class ValidationDataService {
  public dataLoaded: Boolean = false;

  constructor(
    private _http: HttpClient,
    private _configService: ConfigService
  ) {}

  buildQueryUrl(params): HttpParams {
    let queryUrl = new HttpParams();
    for (let key in params) {
      if (isArray(params[key])) {
        queryUrl = queryUrl.set(key, params[key]);
      } else {
        queryUrl = queryUrl.set(key, params[key]);
      }
    }
    return queryUrl;
  }

  getSyntheseData(params) {
    return this._http.get<any>(
      `${this._configService.getSettings("API_ENDPOINT")}/validation`,
      {
        params: this.buildQueryUrl(params)
      }
    );
  }

  getValidationHistory(uuid_attached_row) {
    return this._http.get<any>(
      `${this._configService.getSettings(
        "API_ENDPOINT"
      )}/validation/history/${uuid_attached_row}`,
      {}
    );
  }

  postStatus(data: any, endpoint: Array<number>) {
    const urlStatus = `${this._configService.getSettings(
      "API_ENDPOINT"
    )}/validation/${endpoint}`;
    return this._http.post<any>(urlStatus, data);
  }

  getDefinitionData() {
    return this._http.get<any>(
      `${this._configService.getSettings(
        "API_ENDPOINT"
      )}/validation/definitions`
    );
  }

  getValidationDate(uuid) {
    return this._http.get<any>(
      `${this._configService.getSettings(
        "API_ENDPOINT"
      )}/validation/date/${uuid}`
    );
  }

  getStatusNames() {
    return this._http.get<any>(
      `${this._configService.getSettings(
        "API_ENDPOINT"
      )}/validation/statusNames`
    );
  }

  getTaxonTree() {
    return this._http.get<any>(
      `${this._configService.getSettings("API_ENDPOINT")}/synthese/taxons_tree`
    );
  }

  getOneSyntheseObservation(id_synthese) {
    return this._http.get<any>(
      `${this._configService.getSettings(
        "API_ENDPOINT"
      )}/synthese/vsynthese/${id_synthese}`
    );
  }
}
