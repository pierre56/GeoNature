import { Component, OnInit } from '@angular/core';

import { CruvedStoreService } from '../services/cruved-store.service';
import { ConfigService } from '@geonature/utils/configModule/core';

@Component({
  selector: 'pnx-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss'],
  providers: []
})
export class AdminComponent implements OnInit {
  URL_NOMENCLATURE_ADMIN: string;

  URL_BACKOFFICE_PERM: string;
  constructor(public _cruvedStore: CruvedStoreService, private _configService: ConfigService) {
    const API_ENDPOINT = this._configService.getSettings('API_ENDPOINT');
    this.URL_NOMENCLATURE_ADMIN = API_ENDPOINT + '/admin/';
    this.URL_BACKOFFICE_PERM = API_ENDPOINT + '/permissions_backoffice/users';
  }

  ngOnInit() {}
}
